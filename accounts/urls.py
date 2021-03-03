from django.urls import path

from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),

    path('products/', views.products, name="products"),
    path('product_details/<str:pk>', views.productDetails, name="product_detail"),
    path('customer/<str:pk>', views.customer, name="customer"),

 	# path('create_order/<str:pk>', views.createOrder, name="create_order"),
 	path('update_order/<str:pk>', views.updateOrder, name="update_order"),
 	path('delete_order/<str:pk>', views.deleteOrder, name="delete_order"),

 	path('store/', views.store, name="store"),
 	path('cart/', views.cart, name="cart"),
 	path('checkout/', views.checkout, name="checkout"),
 	path('update_item/', views.updateItem, name="update_item"),
 	path('process_order/', views.processOrder, name="process_order"),

 	path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), 
 		name="reset_password"),
 	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
 		name="password_reset_done"),
 	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
 		name="password_reset_confirm"),
 	path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
 		name="password_reset_complete"),

 	path('delete_product/<str:pk>', views.deleteProduct, name="delete_product"),
 	path('edit_product/<str:pk>', views.editProduct, name="edit_product"),
 	path('update_product/', views.updateProduct, name="update_product"),
 	path('add_products/', views.addProducts, name="add_products"),
 	path('aog_all/', views.aogAll, name="aog_all"),
 	path('update_aog_all/', views.updateAogAll, name="update_aog_all"),
 	path('product_aog/<str:pk>', views.productAog, name="product_aog"),
 	path('update_product_aog/', views.updateProductAog, name="update_product_aog"),

 	path('order_detail/<str:pk>', views.orderDetails, name="order_detail"),
 	path('update_user/<str:pk>', views.updateUser, name="update_user"),
 	
 	path('update_customer/<str:pk>', views.customerSettings, name="update_customer"),
	path('account/', views.accountSettings, name="account"),
 	
 	path('add_tag/', views.addTag, name="add_tag"),
  	path('recover_product/', views.recoverProduct, name="recover_product"),	
 	path('update_recover_product/', views.updateRecoverProduct, name="update_recover_product"),

 	path('about_us/', views.aboutUs, name="about_us"),
 	path('contact_us/', views.contactUs, name="contact_us"),
 ]
handler404 = 'accounts.views.handler404'
handler500 = 'accounts.views.handler500'