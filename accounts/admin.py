from django.contrib import admin

# Register your models here.
# from .models import Customer
from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(OperationHistory)
admin.site.register(PointsHistory)