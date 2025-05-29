from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.forms import modelformset_factory
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from homepage.models import *
from .forms import *
from func.func import *


ImageUploadFormSet = modelformset_factory(Image, CreateImgForm, extra=0, can_delete=True)

def settingsPage(request):
    return redirect('settingspage:gerenalPage')


# ProductPage
def ProductManager(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    context = {
        'acc' : acc,
        'user' : user
    }
    return render(request, 'products/product.html', context)

# tạo sản phẩm mới
class CreateProduct(View):
    def get(self, request):
        form_product = ProductForm()
        acc = Account.objects.get(user_ptr=request.user)
        context = {
            'acc' : acc,
            'form_product':form_product
        }
        return render(request, 'products/addproduct.html', context)
    def post(self, request):
        acc = Account.objects.get(user_ptr=request.user)
        if acc.role == 'sharer':
            return HttpResponse("You need to be a Manager to do this!")
        else:
            user = Manager.objects.get(account = acc)
            newProduct = Product.objects.create(provider = user)
            form_product = ProductForm(request.POST, request.FILES, instance=newProduct)
            if form_product.is_valid():
                # if form_product.cleaned_data['img'].name == 'default.jpg':
                #     messages.error(request, "Please provide a picture for the dish!")
                #     newProduct.delete()
                #     return redirect('settingspage:product')
                product = form_product.save(commit=False)
                product.save()
                messages.success(request, "Dish added successfully!")
            else:
                newProduct.delete()
                messages.error(request, "Dish was not added!")
            return redirect('settingspage:product')


#Xóa Sản phẩm
@csrf_exempt
def deleteProduct(request, product_id):
    try:
        if request.method == 'POST':
            product = Product.objects.get(pk = product_id)
            product.delete()
            return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': 'error'})

# Sửa sản phẩm
class editProduct(View):
    def get(self, request, product_id):
        acc = Account.objects.get(user_ptr=request.user)
        user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
        _product = Product.objects.get(pk = product_id)
        pform = ProductForm(instance= _product)
        context = {
            'form_product': pform,
            'acc': acc,
        }
        return render(request, 'products/addproduct.html', context)
    def post(self, request, product_id):
        _product = Product.objects.get(pk = product_id)
        pform = ProductForm(request.POST, request.FILES, instance = _product)
        if pform.is_valid():
            pform.save()
            messages.success(request, "Đã lưu thay đổi")
        else :
            messages.error(request, "Thực hiện bị lỗi")
        return redirect('settingspage:product')

#generalPage
def generalPage(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)

    if request.method == 'POST':
        if acc.role == 'sharer':
            user.name = request.POST.get('name')
            user.age = request.POST.get('age')
            user.bio = request.POST.get('comment')

            city_id = request.POST.get('city')
            district_id = request.POST.get('district')
            ward_id = request.POST.get('ward')

            user.city, user.district, user.ward = getArea(city_id, district_id, ward_id)

            if 'avatar' in request.FILES:
                user.avatar = request.FILES.get('avatar')
            user.save()
            context = {
                'role': acc.role,
                'acc': acc,
                'user': user,
            }
            return render(request, 'general/general.html', context)
        else:
            user.name = request.POST.get('name')
            user.phone = request.POST.get('phone')
            user.address = request.POST.get('address')
            user.bio = request.POST.get('comment')
            user.t_open = request.POST.get('t_open')
            user.t_closed = request.POST.get('t_closed')

            city_id = request.POST.get('city')
            district_id = request.POST.get('district')
            ward_id = request.POST.get('ward')

            user.city, user.district, user.ward = getArea(city_id, district_id, ward_id)
            if 'avatar' in request.FILES:
                user.avatar = request.FILES.get('avatar')
            if 'bank' in request.FILES:
                user.bank = request.FILES.get('bank')
            user.facebook_link = request.POST.get('facebook_link')
            user.website_link = request.POST.get('website_link')
            user.save()
            context = {
                'role': acc.role,
                'acc': acc,
                'user': user,
                'time_open': user.t_open,
                'time_close': user.t_closed,
            }

            return render(request, 'general/general.html', context)
    if acc.role == 'manager':   
        time_open = user.t_open.strftime("%H:%M")
        time_close = user.t_closed.strftime("%H:%M")

        context = {
            'role': acc.role,
            'acc': acc,
            'user': user,
            'time_open': time_open,
            'time_close': time_close,
        }
    else:
        context = {
            'role': acc.role,
            'acc': acc,
            'user': user,
        }
    return render(request, 'general/general.html', context)


# postPage
def postPage(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    postList = acc.post_set.all()
    context = {
        'acc': acc,
        'user': user,
        'postList': postList,
    }
    return render(request, 'posts/postList.html', context)

def editPost(request, postId):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account=acc) if acc.role=='sharer' else Manager.objects.get(account=acc) 
    if request.method == 'GET':
        post = Post.objects.get(id=postId)
        img = post.image_set.all()
        form_img = []
        a = 0
        for i in img :
            a = a + 1
            form_img.append(CreateImgForm(instance=i, prefix=f'form-{a}'))
        context = {
            'user': user,
            'post': post,
            'img': img,
            'form_img': form_img,
            'provider': Manager.objects.all()
        }
        return render(request, 'posts/edit_post.html', context)
    elif request.method == 'POST':
        post = Post.objects.get(id=postId)
        post.title = request.POST.get('title_post')
        post.content = request.POST.get('content_post')
        if request.POST.get('provider_post') != 'None':
            post.provider_id = request.POST.get('provider_post')
        else:
            post.provider_id = None
        img = post.image_set.all()
        form_img = []
        
        a = 0
        for i in img :
            a = a+1
            if i.isDelete == True :
                i.delete()
            else :
                form_img.append(CreateImgForm(request.POST, request.FILES, prefix=f'form-{a}', instance=i))
        for form in form_img:
            form.save()
        images = request.FILES.getlist('images')
        for image in images :
            img = Image.objects.create(post = post, img = image)
            img.save()

        city_id = request.POST.get('city')
        district_id = request.POST.get('district')
        ward_id = request.POST.get('ward')
        
        post.address = request.POST.get('address_post')
        post.city, post.district, post.ward = getArea(city_id, district_id, ward_id)
        post.save()
        return redirect('settingspage:postPage')
    
def deleteImagePost(request, postId, imageId):
    try:
        image = Image.objects.get(id = imageId)
        image.isDelete = True
        image.save()
        # JsonResponse()
        return HttpResponseRedirect(reverse('settingspage:editPost', args=[postId]))
    except:
        messages.error(request, 'Error')
        # JsonResponse()
        return HttpResponseRedirect(reverse('settingspage:editPost', args=[postId]))


def recoverDelete(request, postId):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account=acc) if acc.role=='sharer' else Manager.objects.get(account=acc) 
    post = Post.objects.get(id=postId)
    img = post.image_set.all()
    for i in img : 
        i.isDelete = False
        i.save()
    return redirect('settingspage:postPage')

def createPost(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account=acc) if acc.role=='sharer' else Manager.objects.get(account=acc)
    if request.method == 'POST':
        post = Post.objects.create(account = acc)
        post.title = request.POST.get('title_post')
        post.content = request.POST.get('content_post')
        if request.POST.get('provider_post') != 'None':
            post.provider_id = request.POST.get('provider_post')
        post.time = timezone.datetime.now()
        images = request.FILES.getlist('images')
        for image in images :
            img = Image.objects.create(post = post, img = image)
            img.save()
        city_id = request.POST.get('city')
        district_id = request.POST.get('district')
        ward_id = request.POST.get('ward')
        
        post.address = request.POST.get('address_post')
        post.city, post.district, post.ward = getArea(city_id, district_id, ward_id)

        post.save()
        return redirect('settingspage:postPage')
    else:
        context = {
            'acc': acc,
            'user': user,
            'time' : timezone.datetime.now(),
            'provider': Manager.objects.all()
        }
        return render(request, 'posts/add_post.html', context)

@csrf_exempt
def deletePost(request, postId):
    try:
        if request.method == 'POST':
            post = Post.objects.get(id=postId)
            post.delete()
            return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': 'error'})
