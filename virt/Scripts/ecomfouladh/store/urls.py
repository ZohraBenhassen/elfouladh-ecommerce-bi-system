from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('search/', views.search, name='search'),
    path('reclam/', views.reclam, name="reclam"),
    path('reclamation', views.send_reclamation, name='send_reclamation'),
    path('dirgen/', views.dirgen, name="dirgen"),
    path('sdvente/', views.sdvente, name='sdvente'),
    path('livreur/', views.livreur, name='livreur'),
    path('orders/', views.orders, name='orders'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product-add'),
    path('products/<int:pk>/', views.ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('profile/', views.profile, name='profile'),
    path('mark-as-delivered/<int:order_id>/', views.mark_as_delivered, name='mark_as_delivered'),
    path('mark-as-not-delivered/<int:order_id>/', views.mark_as_not_delivered, name='mark_as_not_delivered'),
    path('mark_as_in_progress/<int:order_id>/', views.mark_as_in_progress, name='mark_as_in_progress'),
    path('contact/', views.contact, name='contact'),
    path('cmdpasse', views.cmdpasse, name='cmdpasse'),
    path('ca', views.ca, name='ca'),
    path('quvendu', views.quvendu, name='quvendu'),
    path('predi', views.predi, name='predi'),

    path('categories/', views.category_list, name='category-list'),
    path('categories/add/', views.add_category, name='category-add'),
    path('categories/edit/<int:pk>/', views.edit_category, name='category-edit'),
    path('categories/delete/<int:pk>/', views.delete_category, name='category-delete'),

    path('request/', views.request_account, name='request_account'),
    path('request/success/', views.account_request_success, name='account_request_success'),
    path('review/', views.review_requests, name='review_requests'),
    path('approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('clients/', views.client_list, name='client_list'),

    path('my-orders/', views.my_orders, name='my_orders'),
    path('add-comment/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('admin1/', views.admin1, name='admin1'),

    path('profile1/', views.profile1, name='profile1'),
    path('profile2/', views.profile2, name='profile2'),
    path('profile3/', views.profile3, name='profile3'),

]