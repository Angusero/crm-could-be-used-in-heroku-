from django.forms import ModelForm
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django import forms
# import default django user model(what we see in the admin panel)
from django.contrib.auth.models import User


class OrderForm(ModelForm):
	"""docstring for OrderFomr"""
	class Meta:
		model = Order
		# if we just want one or two fields, do fiekds = ['customer', 'status']
		fields = ['status', 'note']


class CreateUserForm(UserCreationForm):
	class Meta():
		model = User
		# python list, you can read the documentation to know what the fields called 
		fields = ['username', 'email','password1','password2']


class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user','points']


class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = '__all__'
		exclude = ['is_deleted']


class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['groups','is_staff']

	# def __init__(self, *args, **kwargs):
	# 	super(UserForm, self).__init__(*args, **kwargs)
	# 	instance = getattr(self, 'instance', None)
	# 	if instance and instance.pk:
	# 		self.fields['username'].disabled = True


class ProductEditForm(ModelForm):
	class Meta:
		model = Product
		fields = '__all__'
		exclude = ['is_deleted']

