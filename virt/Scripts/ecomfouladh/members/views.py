from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .forms import UserCreationForm, ProfileForm
from .models import Profile as MembersProfile
from store.models import Profile as StoreProfile
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from cart.models import Order
import json
from cart.cart import Cart
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail





def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('admin:index')
            elif user.is_staff:
                return redirect('dirgen')
            else:
                # Check if user has a profile in the members app
                try:
                    members_profile = MembersProfile.objects.get(user=user)
                    return redirect_user_by_role(user)
                except MembersProfile.DoesNotExist:
                    pass

                # Check if user has a profile in the store app
                try:
                    store_profile = StoreProfile.objects.get(user=user)
                    saved_cart = store_profile.old_cart
                    if saved_cart:
                        converted_cart = json.loads(saved_cart)
                        cart = Cart(request)
                        for key, value in converted_cart.items():
                            cart.db_add(product=key, quantity=value)
                    messages.success(request, "Vous êtes connecté !")
                    return redirect('home')
                except StoreProfile.DoesNotExist:
                    pass

                # Handle users without any profile
                messages.success(request, "Vous êtes connecté mais sans profil !")
                return redirect('home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return redirect('login')

    return render(request, 'login.html')







def redirect_user_by_role(user):
    if user.members_profile.role == 'admin':
        return redirect('admin_dashboard')
    elif user.members_profile.role == 'sdvente':
        return redirect('sdvente_dashboard')
    elif user.members_profile.role == 'dirgen':
        return redirect('dirgen_dashboard')
    elif user.members_profile.role == 'livreur':
        return redirect('livreur_dashboard')
    else:
        return redirect('login1')

















# @user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']
            user.set_password(password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            # Send welcome email
            subject = 'Bienvenue chez Elfouladh'
            message = f'Bonjour {user.username},\n\nVotre compte a été créé avec succès. Voici vos informations de connexion:\n\nNom d\'utilisateur: {user.username}\nMot de passe: {password}\n\nBienvenue!\n\nCordialement,'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            
            return redirect('users_list')
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'create_user.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })





@login_required
@user_passes_test(lambda u: u.members_profile.role == 'admin')
def admin_dashboard(request):
    # Admin dashboard logic
    return render(request, 'admin.html')

@login_required
@user_passes_test(lambda u: u.members_profile.role == 'sdvente')
def sdvente_dashboard(request):
    # Sales dashboard logic
    return render(request, 'sdvente.html')

@login_required
@user_passes_test(lambda u: u.members_profile.role == 'dirgen')
def dirgen_dashboard(request):
    # Director General dashboard logic
    return render(request, 'dirgen.html')

@login_required
@user_passes_test(lambda u: u.members_profile.role == 'livreur')
def livreur_dashboard(request):
    orders=Order.objects.all()
    return render(request, 'livreur.html', {'orders': orders})





def users_list(request):
    profiles = MembersProfile.objects.exclude(role='')
    return render(request, 'users_list.html', {'profiles': profiles})

def delete_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect('users_list')

def change_role(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        new_role = request.POST.get('new_role')
        profile = MembersProfile.objects.get(user=user)
        profile.role = new_role
        profile.save()
    return redirect('users_list')