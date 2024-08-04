from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
	shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nom complet'}), required=True)
	shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=True)
	shipping_num = forms.CharField(label="", max_length=15, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Numéro de téléphone','type': 'tel','pattern': '[0-9]+'}),required=False)
	shipping_card = forms.CharField(label="", max_length=15, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Numéro de la carte','type': 'tel','pattern': '[0-9]+'}),required=False)
	shipping_numsec = forms.CharField(label="", max_length=15, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Code de sureté','type': 'tel','pattern': '[0-9]+'}),required=False)
	shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adresse'}), required=True)
	shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ville'}), required=True)
	shipping_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Code postal'}), required=False)
	
	class Meta:
		model = ShippingAddress
		fields = ['shipping_full_name','shipping_num',  'shipping_card',  'shipping_numsec',  'shipping_email', 'shipping_address1', 'shipping_city', 'shipping_zipcode']

		exclude = ['user',]
