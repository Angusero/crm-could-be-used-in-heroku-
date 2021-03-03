from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from datetime import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
# Create your models here.

# class Profile(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
# 	first_name = models.CharField(max_length=200, null=True, blank=True)
# 	last_name = models.CharField(max_length=200, null=True, blank=True)
# 	phone = models.CharField(max_length=200, null=True, blank=True)

# 	def __str__(self):
# 		return self.first_name
	
# def create_profile(sender, instance, created, **kwargs):
		

# def update_profile():
# 	pass


class Customer(models.Model):
	# CASCADE: once a user is deleted, the customer related to it would also be deleted
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	"""docstring for Customer"""
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	profile_pic = models.ImageField(default="profile1.png",null=True, blank=True)
	points = models.FloatField(null=True,default=0.00)
	# show the customer name rather than "Customer object" in the admin panel
	def __str__(self):
		return str(self.name)

	@property
	def profile_pic_URL(self):
		try:
			url = self.profile_pic.url
		except:
			url = 'static/images/profile1.png'
		return url

class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)
	"""docstring for Tag"""
	def __str__(self):
		return self.name


def get_or_create_default_tags():
    default_tag1, _ = Tag.objects.get_or_create(name='ALL')
    default_tag2, _ = Tag.objects.get_or_create(name='ALL')
    return default_tag1, default_tag2

class Product(models.Model):
	CATEGORY = (
		('Indoor', 'Indoor'),
		('Outdoor', 'Outdoor'),
		)
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	quantity = models.IntegerField(default=0)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add = True)
	# tags = models.ManyToManyField(Tag, verbose_name='tag', default=get_or_create_default_tags, blank=True)
	tags = models.ManyToManyField(Tag, blank=True)
	digital = models.BooleanField(default=False, null=True,blank=True)
	image = models.ImageField(null=True, blank=True)
	is_deleted = models.BooleanField(default=False)
	
	def __str__(self):
		return self.name
	
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = '../static/images/placeholder.png'
		return url
		
	@property
	def points(self):
		points = float(self.price/100)
		return points
	

class Order(models.Model):
	# create a drop down menu
	STATUS = (
		('Pending', 'Pending'),
		('Out for delivery', 'Out for delivery'),
		('Delivered', 'Delivered'),
		)
	# one to many relastionships
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	# product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	date_created = 	models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True, blank=True)
	is_deleted = models.BooleanField(default=False)

	# from store
	transaction_id = models.CharField(max_length=100, null=True)
	complete = models.BooleanField(default=False)
	# custom attribution
	points = models.FloatField(null=True, default=0.00)

	def __str__(self):
		return str(self.id)
		# return self.product.name

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
	
	@property
	def get_total(self):
		total  = self.product.price * self.quantity
		return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)
	# if user is logged in and the phone number is registered, default show the number
	phone = models.CharField(max_length=200, null=False)

	@property
	def placedtime(self):
		return self.date_added.strftime('%B %d %Y')
	
	# def __str__(self):
	# 	return str(self.order.id)
		# return 'orderId is '+ str(self.order.id)


class OperationHistory(models.Model):
	# user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	operation = models.CharField(max_length=1000, null=False)
	date_added = models.DateTimeField(auto_now_add=True)


def inTwoYears():
	return datetime.now()+relativedelta(years=2)

class PointsHistory(models.Model):
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	point_use = models.FloatField(null=True, default=0.00)
	point_add = models.FloatField(null=True, default=0.00)
	points_after = models.FloatField(null=True, default=0.00)
	expiration_date = models.DateTimeField(default=inTwoYears)
	date_created = models.DateTimeField(auto_now_add = True)

class ErrorRecord(models.Model):
	customerOfUser = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	functionName = models.CharField(max_length=200, null=False)
	targetCustomer = models.CharField(max_length=200, null=False)
	wrongPramaReference = models.CharField(max_length=200, null=False)
	errorContent = models.CharField(max_length=1000, null=False)