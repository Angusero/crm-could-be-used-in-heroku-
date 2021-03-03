from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer

def customer_profile(sender, instance, created, **kwargs):
	if created:
		# automatically socialated the created user as a customer group account
		group = Group.objects.get(name='customer')
		instance.groups.add(group)
		# email = form.cleaned_data.get('email')
		Customer.objects.create(user=instance, name=instance.username, email=instance.email)
		print('profile created')
post_save.connect(customer_profile, sender=User)