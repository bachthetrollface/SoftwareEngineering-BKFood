from django.db import models
import os
from unidecode import unidecode
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import django.db.models.deletion
from django.db.models import Avg
from django.utils import timezone
import uuid

# Create your models here.
def img_path_avt(instance, filename):
    acc = instance.account
    username = acc.username
    role = acc.role
    ext = filename.split('.')[-1]
    new_filename = f"avatar.{ext}" # rename image file
    return os.path.join(role, username , new_filename)

def img_path_bank(instance, filename):
    acc = instance.account
    username = acc.username
    role = acc.role
    ext = filename.split('.')[-1]
    new_filename = f"bank.{ext}"
    return os.path.join(role, username , new_filename)

def imgs_path(instance, filename):
    post_name = str(instance.post)
    username = str(instance.post.account)
    role = instance.post.account.role
    return os.path.join(role, username , 'posts', post_name, filename)

def img_path_bill(instance, filename):
    provider_name = str(instance.provider)
    acc_name = str(instance.acc)
    time = instance.time
    ext = filename.split('.')[-1]
    new_filename = f"{time}_{acc_name}.{ext}"
    return os.path.join('manager', provider_name, 'bills', new_filename)

def img_path_product(instance, filename):
    username = instance.provider.account.username
    product_name = instance.name
    ext = filename.split('.')[-1]
    new_filename = f"{product_name}.{ext}"
    return os.path.join('manager', username, 'products', new_filename)

def generate_unique_post_id():
    return str(uuid.uuid4())


class Account(User):
    ROLES = [
        ('sharer', 'Người chia sẻ'),
        ('manager', 'Người quản lý'),
    ]
    raw_password = models.CharField(max_length=50, null=True)
    role = models.CharField(max_length=10, choices=ROLES)

    def __str__(self):
        return f"{self.username}"


class Sharer(models.Model):
    account = models.OneToOneField(Account, on_delete=django.db.models.deletion.CASCADE, primary_key=True)
    name = models.CharField(verbose_name='fullname', max_length=50)
    age = models.IntegerField(null = True)
    avatar = models.ImageField(upload_to=img_path_avt, default='noavatar.png')

    city = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)
    ward = models.CharField(max_length=50, null=True)

    bio = models.TextField(max_length=1500, null = True)

    def __str__(self):
        return f"{self.account}"

class Manager(models.Model):
    account = models.OneToOneField(Account, on_delete=django.db.models.deletion.CASCADE, primary_key=True)

    name = models.TextField(max_length=50)
    name_stripped = models.TextField(max_length=50, null=True)

    phone = models.CharField(max_length=15, null=True)
    avatar = models.ImageField(upload_to=img_path_avt, default='noavatar.png')
    bank = models.ImageField(upload_to=img_path_bank, default='noavatar.png')
    facebook_link = models.URLField(max_length=200, blank=True, null=True)
    website_link = models.URLField(max_length=200, blank=True, null=True)
    t_open = models.TimeField(default='0:00')
    t_closed = models.TimeField(default='23:59')

    address = models.TextField(null=True)
    city = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)
    ward = models.CharField(max_length=50, null=True)

    bio = models.TextField(max_length=1500, null=True)

    num_votes = models.IntegerField(null=True, default=0)
    avgStar = models.FloatField(default=0.0)


    def __str__(self):
        return f"{self.account}"

    def updateAvgStar(self):
        self.num_votes = self.starvote_set.count()
        avg_star = StarVote.objects.filter(manager=self).aggregate(Avg('stars'))['stars__avg']
        self.avgStar = round(avg_star,1) if avg_star else 0.0

    def save(self, *args, **kwargs):
        self.updateAvgStar()
        if self.name:
            words = unidecode(self.name.lower()).split()
            self.name_stripped = ' '.join(words)
        super().save(*args, **kwargs)


class Product(models.Model):
    TYPES = [
        ('drink', 'Đồ uống'),
        ('food', 'Đồ ăn'),
        ('entertainment', 'Giải trí'),
        ('service', 'Dịch vụ khác'),
    ]
    provider = models.ForeignKey(Manager, on_delete=models.CASCADE)

    name = models.TextField(max_length=50)
    name_stripped = models.TextField(max_length=50, null=True)

    type = models.CharField(max_length=20, choices=TYPES)
    price = models.IntegerField(default=0)
    img = models.ImageField(upload_to=img_path_product, default='default.jpg')
    describe = models.TextField(null=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.datetime.now())

    def __str__(self):
        return f"{self.provider}_{self.name}"

    def save(self, *args, **kwargs):
        if self.name:
            words = unidecode(self.name.lower()).split()
            self.name_stripped = ' '.join(words)
        super().save(*args, **kwargs)


class Bill(models.Model):
    STATUS = [

    ]
    acc = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name='Người mua')
    provider = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(default=timezone.datetime.now())
    price = models.IntegerField(default=0)
    img = models.ImageField(upload_to=img_path_bill, null=True, blank=True)
    status = models.CharField(max_length=200, choices=STATUS, default='Waiting')

    def __str__(self):
        return f"{self.provider}_{self.acc}_" + datetime.strftime(self.time, "%Y-%m-%d %H:%M:%S")

class Order(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product}_{self.bill}"


class Post(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    name_stripped = models.CharField(max_length=150000, null=True)
    time = models.DateTimeField(default=timezone.datetime.now())

    address = models.TextField(null=True)
    city = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)
    ward = models.CharField(max_length=50, null=True)

    provider = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    commentNum = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.account}_{self.title}"

    def save(self, *args, **kwargs):
        words = unidecode((self.title + " " + self.content).lower()).split()
        self.name_stripped = ' '.join(words)

        likeList = UserLike.objects.filter(post = self)
        self.like = likeList.count()
        super().save(*args, **kwargs)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(upload_to=imgs_path)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.post}"


# vote_profile_model
class StarVote(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.account} Voted For {self.manager}"


# like + comment
class UserLike(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null= True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    # class Meta:
    #     # primary key ( account,post)
    #     constraints = [
    #         models.UniqueConstraint(fields=['account_id', 'post_id'], name='unique_constraint_name')
    #     ]

class Comment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=django.db.models.deletion.CASCADE)
    time = models.DateTimeField(default=timezone.datetime.now())
    content = models.TextField()
    like = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post}"

    
#Model for chatPage
# class Message(models.Model):
#     sender = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, related_name='send')
#     receiver = models.ForeignKey(Account, on_delete=models.CASCADE, null= False, related_name='recieve')
#     content = models.CharField(max_length=1000)
#     time = models.DateTimeField(default=timezone.datetime.now())
#     def __str__(self):
#         return f"{self.sender} to {self.receiver} ({self.time})"
    
    
# class ImageMessage(models.Model):
#     message = models.ForeignKey(Message, on_delete=models.CASCADE)
#     img = models.ImageField()
