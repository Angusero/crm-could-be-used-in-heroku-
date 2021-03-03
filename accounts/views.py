from django.shortcuts import render, redirect
from django.http import HttpResponse
# register multiple forms once
from django.forms import inlineformset_factory, modelformset_factory
# create user
from django.contrib.auth.forms import UserCreationForm
# import models
from .models import *
# register order form
from .forms import OrderForm, CreateUserForm, CustomerForm, ProductForm, UserForm, ProductEditForm
# filter function
from .filters import OrderFilter, CustomerFilter, ProductFilter
# show flash message in login page and register page
from django.contrib import messages
# import functions about logging in and logging out
from django.contrib.auth import authenticate, login, logout
# login decoator to restrict views 
from django.contrib.auth.decorators import login_required
# 
from django.contrib.auth.models import Group
# import decorateors.py
from .decorators import unauthenticated_user,allowed_users, staff_only, admin_only

# from ecommerce
from .utils import  cartData, guestOrder

import json
from django.http import JsonResponse
import datetime



@unauthenticated_user
def registerPage(request):
	# if a user is logged in, it is restricted to access the register or login page
	# if request.user.is_authenticated:
	# 	# redirect to homepage
	# 	return redirect('home')
	# else:
	form = CreateUserForm()

	if request.method == 'POST':
		# formInfo = request.POST.get('email')
		email = request.POST.get('email')
		if User.objects.filter(email=email).exists():
			messages.info(request, 'The email has been used for another user')
			return redirect('register')

		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			# email = form.cleaned_data.get('email')
			# customer, created = Customer.objects.get_or_create(user=user, name=username, email=email)


			messages.success(request, 'Account was created for '+ username)

			return redirect('login')

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

# the loginPage fucntion is actully passed to the unauthenticated_user function
#  which means in this case the parameter view_function is the loginPage function
@unauthenticated_user
def loginPage(request):
	# if a user is logged in, it is restricted to access the register or login page
	# if request.user.is_authenticated:
	# 	# redirect to homepage
	# 	return redirect('home')
	# else:

	if request.method == 'POST':
		# get username and password from the html(dont forget to add a crsf_token underneath the form to secure the data)
		username = request.POST.get('username')
	
		password = request.POST.get('password')
		# set the user value to authenticate method
		user = authenticate(request, username=username, password=password)
		# check the user is real there before we redirect them
		if user is not None:
			# take the login method here
			login(request, user)

			# print('THE USER NOW IS '+ user.username)
			customer = request.user.customer
			operation='User ' + user.username +', customer name '+customer.name +' logged in.'
			operation_history(customer, operation)


			return redirect('home')
			# if the user doesn't exist, go back to login page and show flash message
		else:	
			messages.info(request, 'Username or password is incorrect')
	context = {}
	return render(request, 'accounts/login.html', context)
@login_required(login_url='login')
def logoutUser(request):
	user = request.user 

	customer = request.user.customer
	operation='User ' + user.username +', customer name '+customer.name +' logged out.'
	operation_history(customer, operation)
	logout(request)
	# if log out, go back to login page
	return redirect('login')

# if the user is not logged in, send it back to the login page
@login_required(login_url='login')
# if we have some staff members we can also allow staff members to access the page 
# by passing multiple roles like allowed_roles=['admin', 'staff']
# @allowed_users(allowed_roles=['admin'])
# after creating the admin_only function, use admin_only instead of allowed_users
@admin_only
@allowed_users(allowed_roles=['admin','staff'])
def home(request):
	orders = Order.objects.all().filter(complete=True, is_deleted=False)
	customers = Customer.objects.all() 

	user = request.user
	group = user.groups.all()[0].name
	groupid = user.groups.all()[0].id

	total_customers = customers.count()
	total_orders = orders.count()

	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	# on_delivery = 0 if orders.filter(status='Out for delivery').count() == 0 else orders.filter(status='Out for delivery').count()
	on_delivery = orders.filter(status='Out for delivery').count()

	data = cartData(request)
	cartItems = data['cartItems']

	customerFilter = CustomerFilter(request.GET, queryset=customers)
	customers = customerFilter.qs
	orderFilter = OrderFilter(request.GET, queryset=orders)
	# orders = myFilter.queryset
	orders = orderFilter.qs

	context = {'customerFilter':customerFilter ,'orderFilter':orderFilter ,'orders':orders, 'customers':customers, 'on_delivery':on_delivery,
	'total_customers':total_customers, 'total_orders':total_orders,
	'delivered':delivered,'pending':pending, 'cartItems':cartItems}

	return render(request, 'accounts/dashboard.html',context)
	# return HttpResponse('home')

# userpage
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all().filter(complete=True, is_deleted=False)

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']

	user = request.user
	group = user.groups.all()[0].name
	groupid = user.groups.all()[0].id


	phone = request.user.customer.phone


	total_orders = orders.count() 
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	on_delivery = 0 if orders.filter(status='Out for delivery').count() == 0 else orders.filter(status='Out for delivery').count()
	

	context = {'orders':orders, 'on_delivery':on_delivery,
	 'total_orders':total_orders,
	'delivered':delivered,'pending':pending, 'cartItems':cartItems, 'phone':phone}
	return render(request, 'accounts/user.html', context)


# if the user is not logged in, send it back to the login page
@login_required(login_url='login')
# if we have some staff members we can also allow staff members to access the page 
# by passing multiple roles like allowed_roles=['admin', 'staff']
@allowed_users(allowed_roles=['admin','staff'])
def products(request):
	
	products = Product.objects.all().filter(is_deleted=False)
	data = cartData(request)
	cartItems = data['cartItems']

	productFilter = ProductFilter(request.GET, queryset=products)
	products = productFilter.qs


	
	# print('the products are ',products)
	# customer = request.user.customer	
	# order, created = Order.objects.get_or_create(customer=customer, complete=False)
	# cartItems = order.get_cart_items

	context = {'productFilter':productFilter, 'products':products, 'cartItems':cartItems}
	return render(request, 'accounts/products.html',context)

# if the user is not logged in, send it back to the login page
@login_required(login_url='login')
# if we have some staff members we can also allow staff members to access the page 
# by passing multiple roles like allowed_roles=['admin', 'staff']
@allowed_users(allowed_roles=['admin','staff'])
def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	# query customer's child objects from model's field 
	orders = customer.order_set.all().filter(complete=True, is_deleted=False)
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)

	# orders = myFilter.queryset
	orders = myFilter.qs

	customer_me = request.user.customer
	user_id = customer.user.id
	if customer.user.groups.exists():
		user_group = customer.user.groups.all()[0].name
	else:
		# user_group = 'None'
		user_group = 'Customer'

	order, created = Order.objects.get_or_create(customer=customer_me, complete=False)
	cartItems = order.get_cart_items

	context = {'user_id':user_id,'user_group':user_group ,'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter,'cartItems':cartItems}
	return render(request, 'accounts/customer.html',context)

# # if the user is not logged in, send it back to the login page
# @login_required(login_url='login')
# # if we have some staff members we can also allow staff members to access the page 
# # by passing multiple roles like allowed_roles=['admin', 'staff']
# @allowed_users(allowed_roles=['admin','staff'])
# def createOrder(request, pk):
# 	# (parent model, child model) from order to customer, 
# 	# field=() tell it which we want to allow for the child field
# 	# OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
# 	OrderFormSet = inlineformset_factory(Customer, Order, fields=('status'), extra=10)
# 	customer = Customer.objects.get(id=pk)
# 	# set a default value
# 	# form = OrderForm(initial={'customer':customer})
# 	# queryset=Order.objects.none() is used to hide orders the customer already have
# 	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
# 	if request.method == 'POST':
# 		# print('Printing POST:', request.POST)
# 		formset = OrderFormSet(request.POST, instance=customer)
# 		if formset.is_valid():
# 			formset.save()
# 			return redirect('/')

# 	context = {'formset':formset}
# 	return render(request, 'accounts/order_form.html', context)

# if the user is not logged in, send it back to the login page
@login_required(login_url='login')
# if we have some staff members we can also allow staff members to access the page 
# by passing multiple roles like allowed_roles=['admin', 'staff']
@allowed_users(allowed_roles=['admin','staff'])
def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	customer = order.customer.name
	transaction_id = order.transaction_id
	user = request.user
	
	if request.method == 'POST':

		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()

			customer_user = request.user.customer
			
			operation='User ' + user.username +', customer name '+customer_user.name+ 'changed the order information [ order id: ' + str(order.id) + ', status: '
			 # + order['status'] + ', note: '+ order.note +' ] into [' + str(order.id) + ', ' +']'
			
			operation_history(customer_user, operation)

			
			return redirect('/')

	context = {'form':form, 'order':order}
	return render(request, 'accounts/order_form.html', context)

# if the user is not logged in, send it back to the login page
@login_required(login_url='login')
# if we have some staff members we can also allow staff members to access the page 
# by passing multiple roles like allowed_roles=['admin', 'staff']
# @admin_only
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	user = request.user 

	data = cartData(request)
	cartItems = data['cartItems']

	if request.method == "POST":
		order.is_deleted = True
		order.save()

		customer = request.user.customer
		operation='User ' + user.username +', customer name '+customer.name +' has deleted the order(order id: ' + str(order.id) + ')'
		operation_history(customer, operation)
		
		# OperationHistory.objects.create(
		# 		user=user,
		# 		operation=user.username + ' has deleted the order(order id: ' + order.id + ')'
		# 		)

		return redirect('/')
	context = {'item':order}
	return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	phone = customer.phone
	user = request.user

	data = cartData(request)
	cartItems = data['cartItems']

	form = CustomerForm(instance=customer)
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid:
			form.save()

			operation='User ' + user.username +', customer name '+customer.name + ' has changed the profile, '
			operation_history(customer, operation)
		
	context={'form':form, 'phone':phone, 'cartItems':cartItems}
	return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['admin'])
def customerSettings(request, pk):
	operator = request.user
	operatorCustomer = request.user.customer

	customer = Customer.objects.get(id=pk)
	user = User.objects.get(customer=customer)
	phone = customer.phone

	data = cartData(request)
	cartItems = data['cartItems']

	form = CustomerForm(instance=customer)


	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		# customer.name = form.name
		# customer.phone= form.phone
		# customer.email= form.email
		# customer.profile_pic= form.profile_pic
		if form.is_valid:
			form.save()

			operation='User ' + operator.username +', customer name '+operatorCustomer.name + ' has changed profile of '+user.username
			operation_history(customer, operation)
		
	context={'form':form, 'phone':phone, 'customer':customer, 'cartItems':cartItems}
	return render(request, 'accounts/customer_settings.html', context)


@login_required(login_url='login')
def store(request):
	
	# products = Product.objects.all().filter(is_deleted=False).filter(quantity__gt=0)
	products = Product.objects.all().filter(is_deleted=False)

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']		
	

	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'accounts/store.html', context)

@login_required(login_url='login')
def cart(request):
	
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products=Product.objects.filter(id__in = [item.product.id for item in items])

	context = {'items':items, 'order':order, 'cartItems':cartItems,'products':products}
	return render(request, 'accounts/cart.html', context)

@login_required(login_url='login')
def checkout(request):

	customer = request.user.customer	
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	items = order.orderitem_set.all()
	cartItems = order.get_cart_items
	address = ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address='',
			city='',
			state='',
			zipcode='',
		)
	if ShippingAddress.objects.all().count()>0:
		address = ShippingAddress.objects.filter(customer=customer).order_by('-date_added')[0]

	context = {'items':items, 'order':order, 'cartItems':cartItems, 'customer':customer, 'address':address}
	return render(request, 'accounts/checkout.html', context)

@login_required(login_url='login')
def updateItem(request):
	data =json.loads(request.body)
	productId = data['productId']
	action = data['action']


	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		if orderItem.quantity == product.quantity:
			orderItem.quantity = product.quantity
		else:
			orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	# print(orderItem.product , ' $$$$$$ ', orderItem.quantity)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


@login_required(login_url='login')
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	
	customer = request.user.customer

	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	total = float(data['form']['total'])
	order.points = float(data['form']['order_points'])
	order.transaction_id = transaction_id

	points_to_use = float(data['pointsInfo']['points_to_use'])
	new_added_points = float(data['pointsInfo']['new_added_points'])
	

	customer.points = round((customer.points + new_added_points - points_to_use),2)
	customer.save()
		
	PointsHistory.objects.create(
		order=order, 
		customer=customer,
		point_use=points_to_use,
		point_add=new_added_points,
		points_after=customer.points,
		)


	if total == order.get_cart_total:
		order.complete = True
		order.status = 'Pending'

	order.save()

	items = order.orderitem_set.all()

	print('ALL ITEMS ARE HERE:',items)


	for item in items:
		productId = item.product.id
		product = Product.objects.get(id=productId)
		product.quantity = product.quantity - item.quantity

		product.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
	return JsonResponse('Payment subbmitted...', safe=False)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def deleteProduct(request, pk):
	product = Product.objects.get(id=pk)
	user = request.user

	data = cartData(request)
	cartItems = data['cartItems']

	if request.method == "POST":
		product.is_deleted = True
		product.name += '(deleted)' 
		product.save()

		customer = request.user.customer
		operation='User ' + user.username +', customer name '+customer.name +' has deleted the product whose ID is: '+ product.id + ', name is: ' +product.name +'.'
		operation_history(customer, operation)

		return redirect('products')
	context = {'item':product, 'cartItems':cartItems}
	return render(request, 'accounts/delete_product.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def editProduct(request, pk):

	data = cartData(request)
	cartItems = data['cartItems']

	product = Product.objects.get(id=pk)
	form = ProductForm(instance=product)

	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES, instance=product)
		if form.is_valid:
			form.save()
			return redirect('products')
			# return JsonResponse('product information changed', safe=False)
			# return redirect('products')
	context = {'product':product, 'form':form}
	return render(request, 'accounts/edit_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def updateProduct(request):
	data = json.loads(request.body)
	user = request.user
	customer = request.user.customer

	product = Product.objects.get(id=int(data['productInfo']['id']))
	ProductInfo=data['productInfo']

	txt=''
	if request.method == "POST":
		if product.name != ProductInfo['name'] or str(product.price) != ProductInfo['price'] or  str(product.category) != str(ProductInfo['category']) or product.description != ProductInfo['description']:
			operation='User ' + user.username +', customer name '+customer.name +' has changed the product information: from '+str(product.name)+' '+str(product.price)+' '+str(product.category)+' '+str(product.description)+' to '+str(ProductInfo)
			
			product.name=data['productInfo']['name']
			product.price=data['productInfo']['price']
			product.category=data['productInfo']['category']
			product.description=data['productInfo']['description']
			product.save()

			operation_history(customer, operation)
			txt='Product information is changed'
		else:
			txt='Nothing changed'

	return JsonResponse(txt, safe=False)
	

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def addProducts(request):
	form = ProductForm()
	data = cartData(request)
	cartItems = data['cartItems']

	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('products')
	context = {'form':form}
	return render(request, 'accounts/add_products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def aogAll(request):
	products = Product.objects.all().filter(is_deleted=False).order_by('id')

	data = cartData(request)
	cartItems = data['cartItems']

	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'accounts/aog_all.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def updateAogAll(request):
	data = json.loads(request.body)
	user = request.user
	customer = request.user.customer

	if request.method == 'POST':
		for i in data['quantityArray']:
			product = Product.objects.get(id=int(i['id']))
			quantity_before = product.quantity
			product.quantity = int(i['quantity'])
			product.save()

			operation='User ' + user.username +', customer name '+customer.name +' has updated the product quantity: from '+str(quantity_before)+' to '+str(product.quantity)
			operation_history(customer, operation)

	return JsonResponse('Multiple products quantity Updated', safe=False)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def updateProductAog(request):
	data = json.loads(request.body)
	# print(data)
	user = request.user
	customer = request.user.customer

	product = Product.objects.get(id=int(data['newInstock']['id']))

	if request.method == 'POST':
		quantity_before = product.quantity
		product.quantity = int(data['newInstock']['quantity'])
		product.save()

		operation='User ' + user.username +', customer name '+customer.name +' has updated the product quantity: from '+str(quantity_before)+' to '+str(product.quantity)
		operation_history(customer, operation)

	return JsonResponse('Product quantity is Updated', safe=False)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def productAog(request, pk):

	data = cartData(request)
	cartItems = data['cartItems']

	product = Product.objects.get(id=pk)


	context = {'cartItems':cartItems, 'product':product}
	return render(request, 'accounts/product_aog.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def orderDetails(request, pk):
	order = Order.objects.get(id=pk)
	items = order.orderitem_set.all()
	
	data = cartData(request)
	cartItems = data['cartItems']

	shipping = ShippingAddress.objects.get(order=pk)
	
	context = {'order':order, 'items':items, 'shipping':shipping, 'cartItems':cartItems}
	return render(request, 'accounts/order_detail.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateUser(request, pk):
	
	user = request.user
	userCustomer = Customer.objects.get(user=user)
	userGroup=user.groups.all()[0].name
	
	targetUser= User.objects.get(id=pk)
	targetCustomer = Customer.objects.get(user=targetUser)
	targetUserGroup=targetUser.groups.all()[0].name

	form = UserForm()
	
	if request.method == 'POST':
		form = UserForm(request.POST, instance=targetUser)
		
		if form.is_valid():
			form.save()
			newTargetUserGroup =targetUser.groups.all()[0].name

			operation='User ' + user.username +', customer name '+targetCustomer.name +' has changed the authentication of '+ targetUser.username + ' from ' + targetUserGroup +' to '+newTargetUserGroup
			operation_history(userCustomer, operation)

		return redirect('/')
	

	context = {'user':user, 'userCustomer':userCustomer,'targetUser':targetUser,'targetCustomer':targetCustomer,'form':form,'targetUserGroup':targetUserGroup}
	return render(request, 'accounts/update_user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def recoverProduct(request):
	products = Product.objects.all().filter(is_deleted=True)
	context = {'products':products}
	return render(request, 'accounts/recover_products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def addTag(request):
	user=request.user
	customer = Customer.objects.get(user=user)
	data = json.loads(request.body)
	newTag = data['tag']['newTag']
	Tag.objects.create(name=newTag)
	operation='User '+ user.username + ' added a new Tag: '+ newTag
	operation_history(customer, operation)

	return JsonResponse('Tag added.', safe=False)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def updateRecoverProduct(request):
	data =json.loads(request.body)
	productId = data['productId']
	action = data['action']

	if action == 'recover':
		product = Product.objects.get(id=productId)
		product.is_deleted = False
		product.name = product.name[:-9]
		product.save()

	return JsonResponse('product was recovered', safe=False)

@login_required(login_url='login')
def productDetails(request, pk):
	product = Product.objects.get(id=pk)
	data = cartData(request)
	cartItems = data['cartItems']
	
	context = {'product':product,'cartItems':cartItems}
	return render(request, 'accounts/product_details.html', context)

@login_required(login_url='login')
def aboutUs(request):
	data = cartData(request)
	cartItems = data['cartItems']
	
	context = {'cartItems':cartItems}
	return render(request, 'accounts/about_us.html', context)

@login_required(login_url='login')
def contactUs(request):
	data = cartData(request)
	cartItems = data['cartItems']
	
	context = {'cartItems':cartItems}
	return render(request, 'accounts/contact_us.html', context)


def operation_history(operator, operation):
	OperationHistory.objects.create(
				customer=operator,
				operation=operation
				)


from django.template import RequestContext


def handler404(request, *args, **argv):
    response = render('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response