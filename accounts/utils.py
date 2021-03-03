import json
from .models import *

def cartData(request):
	customer = request.user.customer	

	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	
	items = order.orderitem_set.all()
	cartItems = order.get_cart_items

	return {'items':items, 'order':order, 'cartItems':cartItems}

def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(email=email)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer = customer,
		complete = False,
		)

	# loop through cart items replica list and create real OrderItems by querying the product and setting the nessesary attributes.
	for item in items:
		product = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity'],
			)

	return customer, order
