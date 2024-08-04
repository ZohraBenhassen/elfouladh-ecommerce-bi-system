from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Order
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from cart.models import Order

from .forms import OrderStatusForm
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from .models import AccountRequest, AccountDocument
from django.views.decorators.http import require_POST

from cart.forms import ShippingForm
from cart.models import ShippingAddress, OrderComment

from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

from django.urls import reverse
from .forms import CategoryForm


def reclam(request):
	context = {}
	return render(request, 'reclam.html', context)







def livreur(request):
	orders=Order.objects.all()
	return render(request, 'livreur.html', {'orders': orders})



def dirgen(request):
	context = {}
	return render(request, 'dirgen.html', context)


def predi(request):
	context = {}
	return render(request, 'predi.html', context)



def cmdpasse(request):
	context = {}
	return render(request, 'cmd_passe.html', context)


def quvendu(request):
	context = {}
	return render(request, 'qu_vendu.html', context)


def ca(request):
	context = {}
	return render(request, 'ca.html', context)


def search(request):
    # Check if the request method is POST
    if request.method == "POST":
        # Get the searched term from the POST data
        searched = request.POST.get('searched', '')
        
        # If the searched term is empty, return an empty context
        if not searched:
            messages.success(request, "Veuillez saisir un produit à rechercher..")
            return render(request, "search.html", {'searched': []})
        
        # Query the Product DB Model
        searched_products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        
        # If no products are found, display a message
        if not searched_products:
            messages.success(request, "Ce produit n'existe pas... Veuillez réessayer.")
            return render(request, "search.html", {'searched': []})
        else:
            # If products are found, return them in the context
            return render(request, "search.html", {'searched': searched_products})
    else:
        # If the request method is not POST, render the search page with an empty context
        return render(request, "search.html", {})


def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Vos informations ont été mises à jour !!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form, })
	else:
		messages.success(request, "Vous devez être connecté pour accéder à cette page !!")
		return redirect('home')



def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Votre mot de passe a été mis à jour...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "Vous devez être connecté pour accéder à cette page !!")
		return redirect('home')


def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "L'utilisateur a été mis à jour !!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "Vous devez être connecté pour accéder à cette page !!")
		return redirect('home')


def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {"categories":categories})	

def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("Cette catégorie n'existe pas..."))
		return redirect('home')


def product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'product.html', {'product':product})


def home(request):
	products = Product.objects.all()
	return render(request, 'home.html', {'products':products})


def about(request):
	return render(request, 'about.html', {})

def admin1(request):
	return render(request, 'admin.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("Vous avez été déconnecté... Merci d'être passé..."))
	return redirect('home')



def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Nom d'utilisateur créé - Veuillez remplir vos informations d'utilisateur ci-dessous..."))
			return redirect('update_info')
		else:
			messages.success(request, ("Oups ! Un problème est survenu lors de l'inscription, veuillez réessayer..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})




def send_reclamation(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '')
        email = request.POST.get('email', '')
        telephone = request.POST.get('telephone', '')
        reclamation = request.POST.get('reclamation', '')

        subject = "Nouvelle Réclamation de {}".format(nom)
        message = "Nom: {}\nEmail: {}\nTéléphone: {}\nRéclamation: {}".format(nom, email, telephone, reclamation)
        from_email = email
        to_email = ['benhassenzohra02@gmail.com']

        try:
            send_mail(subject, message, from_email, to_email)
            messages.success(request, "Votre réclamation a été envoyée avec succès.")
        except Exception as e:
            messages.error(request, "Une erreur s'est produite lors de l'envoi de votre réclamation.")
        
        return redirect('home')
    else:
        return redirect('home')





def sdvente(request):
	context = {}
	return render(request, 'sdvente.html', context)


def orders(request):
	orders = Order.objects.all()
	return render(request, 'orders.html', {"orders":orders})

def contact(request):
	context = {}
	return render(request, 'contact.html', context)



class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'  

class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    template_name = 'product_form.html' 
    success_url = reverse_lazy('product-list')

class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'product_form.html'  
    success_url = reverse_lazy('product-list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_delete.html'  
    success_url = reverse_lazy('product-list')


def profile(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request,
		  current_user)
			messages.success(request, "L'utilisateur a été mis à jour !!")
			return redirect("profile")
		return render(request, 'profile.html', {'user_form':user_form})
	else:
		messages.success(request, "Vous devez être connecté pour accéder à cette page !!")
		return redirect(request,'profile.html', {})







def profile1(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request,
		  current_user)
			messages.success(request, "L'utilisateur a été mis à jour !!")
			return redirect("profile1")
		return render(request, 'profile1.html', {'user_form':user_form})
	else:
		messages.success(request, "Vous devez être connecté pour accéder à cette page !!")
		return redirect(request,'profile1.html', {})
	





def profile2(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request,
		  current_user)
			messages.success(request, "L'utilisateur a été mis à jour !!")
			return redirect("profile2")
		return render(request, 'profil2.html', {'user_form':user_form})
	else:
		messages.success(request, "Vous devez être connecté pour accéder à cette page !!")
		return redirect(request,'profil2.html', {})
	





def profile3(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request,
		  current_user)
			messages.success(request, "L'utilisateur a été mis à jour !!")
			return redirect("profile3")
		return render(request, 'profil3.html', {'user_form':user_form})
	else:
		messages.success(request, "Vous devez être connecté pour accéder à cette page !!")
		return redirect(request,'profil3.html', {})













@require_POST
def mark_as_in_progress(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        # if order.status == 'pending':
        order.status = 'in_progress'
        order.save()
    except Order.DoesNotExist:
        return HttpResponseForbidden()
    return redirect('livreur')  

@require_POST
def mark_as_delivered(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        # if order.status == 'in_progress':
        order.status = 'delivered'
        order.save()
    except Order.DoesNotExist:
        return HttpResponseForbidden()
    return redirect('livreur')

@require_POST
def mark_as_not_delivered(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        # if order.status == 'delivered':
        order.status = 'pending'
        order.save()
    except Order.DoesNotExist:
        return HttpResponseForbidden()
    return redirect('livreur')



def request_account(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            # Save account request
            account_request = AccountRequest(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
				password=form.cleaned_data['password1'],
            )
            account_request.save()
            
            # Handle document uploads
            for file in request.FILES.getlist('documents'):
                AccountDocument.objects.create(
                    account_request=account_request,
                    document=file
                )
            
            return redirect('account_request_success')
    else:
        form = SignUpForm()
    return render(request, 'request_account.html', {'form': form})

def account_request_success(request):
    return render(request, 'account_request_success.html')

# @user_passes_test(lambda u: u.is_superuser)
def review_requests(request):
    requests = AccountRequest.objects.filter(is_approved=False, is_rejected=False)
    return render(request, 'review_requests.html', {'requests': requests})

# @user_passes_test(lambda u: u.is_superuser)
def approve_request(request, request_id):
    account_request = AccountRequest.objects.get(id=request_id)
    user = User.objects.create_user(username=account_request.username, email=account_request.email, password=account_request.password)
    account_request.is_approved = True
    account_request.save()
    account_request.send_approval_email()
    return redirect('review_requests')

# @user_passes_test(lambda u: u.is_superuser)
def reject_request(request, request_id):
    account_request = AccountRequest.objects.get(id=request_id)
    account_request.is_rejected = True
    account_request.save()
    account_request.send_rejection_email()
    return redirect('review_requests')











@login_required
def my_orders(request):
    # Retrieve orders associated with the current user
    user_orders = Order.objects.filter(user=request.user)

    return render(request, 'my_orders.html', {'user_orders': user_orders})


@login_required
def add_comment(request):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id, user=request.user)
        OrderComment.objects.create(order=order, user=request.user, comment=comment_text)
        return redirect('my_orders')
    return redirect('my_orders')

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(OrderComment, id=comment_id)
    if request.user != comment.user:
        return redirect('my_orders')
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            comment.comment = comment_text
            comment.save()
    return redirect('my_orders')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(OrderComment, id=comment_id)
    if request.user != comment.user:
        return redirect('my_orders')

    if request.method == 'POST':
        comment.delete()
    return redirect('my_orders')







def client_list(request):
    approved_accounts = AccountRequest.objects.filter(is_approved=True)
    failed_accounts = AccountRequest.objects.filter(is_rejected=True)
    
    context = {
        'approved_accounts': approved_accounts,
        'failed_accounts': failed_accounts
    }
    return render(request, 'client_list.html', context)



def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form})

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    return render(request, 'delete_category.html', {'category': category})