from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings


#category of pt
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name_plural = 'categories'


 
class Customer(models.Model):
    first_name  = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    document = models.FileField(upload_to='uploads/documents/', null=True)
    password = models.CharField(max_length=100)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(default=0, decimal_places=3, max_digits=8)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    quantity = models.FloatField()
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image= models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return self.name
    def is_sold_out(self):
        return self.quantity <= 0

class Users(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200, null=True)    
    password = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name



class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=100, default='', blank=True)
    date = models.DateTimeField(default=datetime.datetime.today) 
    statue = models.BooleanField(default=False)

        
    def __str__(self):
        return {self.product}



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_modified = models.DateTimeField(User, auto_now=True)
	phone = models.CharField(max_length=20, blank=True)
	address1 = models.CharField(max_length=200, blank=True)
	address2 = models.CharField(max_length=200, blank=True)
	city = models.CharField(max_length=200, blank=True)
	state = models.CharField(max_length=200, blank=True)
	zipcode = models.CharField(max_length=200, blank=True)
	country = models.CharField(max_length=200, blank=True)
	old_cart = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.user.username
    


def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)




class AccountRequest(models.Model):
    username = models.CharField(max_length=150, default=False)
    email = models.EmailField(default=False)
    first_name = models.CharField(max_length=100, default=False)
    last_name = models.CharField(max_length=100, default=False)
    password = models.CharField(max_length=48, default='temporary_password')
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def send_approval_email(self):
        subject = 'Votre compte a été approuvé'
        message = f'Votre compte a été approuvé. Votre nom utilisateur est {self.username} et votre mot de passe est : {self.password}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email])

    def send_rejection_email(self):
        subject = 'Votre demande de compte a été rejetée'
        message = 'Votre demande de compte a été rejetée'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email])


class AccountDocument(models.Model):
    account_request = models.ForeignKey(AccountRequest, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/')


