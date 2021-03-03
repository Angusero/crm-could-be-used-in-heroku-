from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	# args:arguments, kwargs:key arguments
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
		# redirect to homepage
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			print('group:',group)
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
				print('groups:', request.user.groups.all())
				print('group:', group)

			if group in allowed_roles:
			# print('Working:', allowed_roles)
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator


def staff_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		# if there are too many groups, dont use this logic
		if group == 'customer':
			return redirect('user-page')
		if group == 'admin' or 'staff':
			return view_func(request, *args, **kwargs)

	return wrapper_func


def admin_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		# if there are too many groups, dont use this logic
		if group == 'customer':
			return redirect('user-page')
		# if group == 'staff':
		# 	return view_func(request, *args, **kwargs)
		if group == 'admin' or 'staff':
			return view_func(request, *args, **kwargs)

	return wrapper_func