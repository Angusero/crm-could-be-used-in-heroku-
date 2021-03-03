import django_filters
from .models import *
from django_filters import DateFilter, CharFilter

class OrderFilter(django_filters.FilterSet):
	# create some custom attritubes
	start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	end_date = DateFilter(field_name="date_created", lookup_expr='lte')

	# icontains means "ignore case sensitivity"
	note = CharFilter(field_name="note", lookup_expr='icontains')
	
	class Meta:
		model = Order
		fields = '__all__'
		exclude = ['customer', 'date_created','is_deleted','complete']



class CustomerFilter(django_filters.FilterSet):
	name = CharFilter(field_name="name", lookup_expr='icontains')
	phone = CharFilter(field_name="phone", lookup_expr='icontains')
	email = CharFilter(field_name="email", lookup_expr='icontains')

	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user', 'date_created','profile_pic','points']


class ProductFilter(django_filters.FilterSet):
	name = CharFilter(field_name="name", lookup_expr='icontains')
	price = CharFilter(field_name="price", lookup_expr='icontains')
	category = CharFilter(field_name="category", lookup_expr='icontains')
	description = CharFilter(field_name="description", lookup_expr='icontains')
	
	class Meta:
		model = Product
		fields = '__all__'
		exclude = ['image','is_deleted','date_created']