from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'settingspage'
urlpatterns = [
    path('', views.settingsPage, name='settingsPage'),
    path('general/', views.generalPage, name='gerenalPage'),

    path('posts', views.postPage, name='postPage'),
    path('posts/addPosts', views.createPost, name='createPost'),
    path('posts/delete/<int:postId>/', views.deletePost, name='deletePost'),
    path('posts/edit/<int:postId>/', views.editPost, name="editPost"),
    path('posts/edit/<int:postId>/testDeleteImagePost/<int:imageId>', views.deleteImagePost, name='deleteImagePost'),
    path('posts/edit/<int:postId>/testRecoverDelete/', views.recoverDelete, name="recoverDelete"),

    path('product/', views.ProductManager, name='product'),
    path('product/add', views.CreateProduct.as_view(), name='addProduct'),
    path('product/delete/<int:product_id>', views.deleteProduct, name='deleteProduct'),
    path('product/edit/<int:product_id>', views.editProduct.as_view(), name='editProduct'),


    # path('bills/', views.billsPage, name='billsPage'),
    # path('bills/viewBill/<int:billId>', views.viewBill, name='viewBill'),
    # path('bills/viewBill/<int:billId>/accept/>', views.accept, name='accept'),
    # path('bills/viewBill/<int:billId>/decline/>', views.decline, name='decline'),


    # path('statistics/', views.statisticsPage, name='statisticsPage'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_URL)