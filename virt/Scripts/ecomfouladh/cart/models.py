from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
import datetime

# Create your models here.

class ShippingAddress(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	shipping_full_name = models.CharField(max_length=255)
	shipping_email = models.CharField(max_length=255,null=True)
	shipping_address1 = models.CharField(max_length=255)
	shipping_num = models.CharField(max_length=255, null=True)
	shipping_city = models.CharField(max_length=255)
	
	shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
	
    
	# Don't pluralize address
	class Meta:
		verbose_name_plural = "Shipping Address"

	def __str__(self):
		return f'{str(self.shipping_address1)} - {str(self.shipping_city)} - {str(self.shipping_zipcode)} - Numéro de téléphone: {str(self.shipping_num)}'

# Create a user Shipping Address by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
	if created:
		user_shipping = ShippingAddress(user=instance)
		user_shipping.save()

# Automate the profile thing
post_save.connect(create_shipping, sender=User)



# Create Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Non Livrée'),
        ('in_progress', 'En cours de livraison'),
        ('delivered', 'Livrée')
    ]

    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order - {str(self.id)}'

# Auto Add shipping Date
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.status == 'delivered' and obj.status != 'delivered':
            instance.date_shipped = now






# Create Order Items Model
class OrderItem(models.Model):
	# Foreign Keys
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	quantity = models.PositiveBigIntegerField(default=1)
	price = models.DecimalField(max_digits=7, decimal_places=2)


	def __str__(self):
		return f'Order Item - {str(self.id)}'



class OrderComment(models.Model):
    order = models.ForeignKey(Order, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment - {str(self.id)}'


