from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from homepage.models import *
import json


def postsPage(request):
    posts = Post.objects.filter().order_by('-time')
    managers = Manager.objects.filter().order_by('-avgStar')
    return render(request, 'index.html', {'posts' : posts, 'managers' : managers})

# Posts -------------------------------------------------------------
def postsView(request):
    posts = Post.objects.filter().order_by('-time')
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    info = list()
    for p in posts:
        author = Sharer.objects.get(account= p.account) if p.account.role == 'sharer' else Manager.objects.get(account= p.account)
        try:
            userLike = UserLike.objects.get(account=acc, post=p)
        except:
            userLike = None
        info.append({
            'post': p,
            'author': author,
            'userLike': userLike,
            'img': Image.objects.filter(post = p)
        })

    context = {
        'acc': acc,
        'user': user,
        'info' : info,
    }
    return render(request, 'posts.html', context)

# Restaurants-----------------------------------------------
def restaurantsView(request):
    '''
    Hiển thị danh sách cửa hàng đã vote sao
    '''
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    managers = Manager.objects.filter().order_by('name')
    context = {
        'acc': acc,
        'user': user,
        'managers' : managers,
    }

    return render(request, 'restaurants.html', context)


@csrf_exempt
def update_likes(request, post_id):
    acc = Account.objects.get(user_ptr=request.user)
    post = Post.objects.get(id = post_id)
    if request.method == 'POST':
        # Nhận dữ liệu từ yêu cầu AJAX
        data = json.loads(request.body)
        if( post.like < data['like'] ):
            userLike = UserLike.objects.create(
                account = acc,
                post = post
            )
            print("Tạo userlike")
        else:
            userLike = UserLike.objects.get(
                account = acc,
                post = post
            )
            userLike.delete()
            print("Xóa userlike")
        post.like = data['like']
        post.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

@csrf_exempt
def insert_comment(request, post_id):
    acc = Account.objects.get(user_ptr=request.user)
    if request.method == 'POST':
        # Nhận dữ liệu từ yêu cầu AJAX
        data = json.loads(request.body)

        post = Post.objects.get(id = post_id)
        comment = Comment.objects.create(
            account = acc,
            post = post,
            time = timezone.now(),
            content = data['comment']
        )
        post.commentNum += 1
        post.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

@csrf_exempt
def delete_comment(request, comment_id):
    acc = Account.objects.get(user_ptr=request.user)
    if request.method == 'POST':
        comment = Comment.objects.get(id = comment_id)
        if comment.account == acc: # chỉ xóa đc comment của mình
            post = comment.post
            post.commentNum -= 1
            post.save()
            comment.delete()
            return JsonResponse({'success': True, 'postId': post.id})
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': "error"})

@csrf_exempt
def get_comments(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post).order_by('-time')
        data = []
        for comment in comments:
            author = Sharer.objects.get(account= comment.account) if comment.account.role == 'sharer' else Manager.objects.get(account= comment.account)
            data.append({
                'id': comment.id,
                'name': author.name,
                'authorId': comment.account.id,
                'img': author.avatar.url,
                'time': comment.time,
                'content': comment.content
            })

        return JsonResponse({'comments': data})
    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({'error': 'An error occurred'})

@csrf_exempt
def searchPosts(request):
    searchKey = request.POST.get('searchKey')
    words = unidecode(searchKey.lower()).split()
    keyword = ' '.join(words)

    dataSearch = []
    for post in Post.objects.filter(name_stripped__icontains=keyword).order_by('-like'):
        if post.account.role == 'manager':
            user = Manager.objects.get(account= post.account)
        else:
            user = Sharer.objects.get(account= post.account)

        dataSearch.append({
            'id': post.id,
            'name': user.name,
            'authorId': post.account.id,
            'avatar': user.avatar.url,
            'title': post.title,
            'address': f"{post.ward} - {post.district}",
            'provider':{
                'name': post.provider.name,
                'id': post.provider.account.id
            } if post.provider else None,
            'like': post.like,
            'cmt': post.commentNum
        })
    print(dataSearch)
    return JsonResponse({'dataSearch': dataSearch})

@csrf_exempt
def detailPost(request, post_id):
    acc = Account.objects.get(user_ptr=request.user)
    user = Manager.objects.get(account = acc) if acc.role == 'manager' else Sharer.objects.get(account = acc) 
    post = Post.objects.get(id=post_id)
    if post.account.role == 'manager':
        author = Manager.objects.get(account = post.account)
    else:
        author = Sharer.objects.get(account = post.account)

    try:
        isLike = UserLike.objects.get(account=acc, post=post)
        isLike = True
    except:
        isLike = False
        
    detailPost = {
        'user': {
            'avatar': user.avatar.url,
        },
        'authorName': author.name,
        'authorAvatar': author.avatar.url,
        'time': post.time,
        'provider': post.provider.name,

        'title': post.title,
        'content': post.content,
        'img': list(),
        'like': post.like,
        'cmt': post.commentNum,

        'userLike': isLike,

    }
    for img in Image.objects.filter(post=post):
        detailPost['img'].append(img.img.url)

    return JsonResponse({'detailPost': detailPost})
