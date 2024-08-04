from django.urls import path
from .views import create_user, login, admin_dashboard, sdvente_dashboard, dirgen_dashboard, livreur_dashboard, users_list, delete_user, change_role

urlpatterns = [
    path('create_user/', create_user, name='create_user'),
    path('login1/', login, name='login'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('sdvente_dashboard/', sdvente_dashboard, name='sdvente_dashboard'),
    path('dirgen_dashboard/', dirgen_dashboard, name='dirgen_dashboard'),
    path('livreur_dashboard/', livreur_dashboard, name='livreur_dashboard'),


    path('users/', users_list, name='users_list'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('users/change_role/<int:user_id>/', change_role, name='change_role'),
]
