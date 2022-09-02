from django.urls import path
#from account.views import afterlogin_view
from . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
	#Leave as empty string for base url
	#path('verify/<int:id>', views.verify),
    path('', views.store, name="store"),
	
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	#path('afterlogin', afterlogin_view,name='afterlogin'),
	path('shipping_info', views.shippingView, name = 'shipping_info'),
	path('logout', LogoutView.as_view(template_name='store/store.html'),name='logout'),
	path('addProduct/', views.addProduct, name='addProduct'),
	path('addCategory/', views.addCategory, name='addCategory'),
	path('updateProduct/<int:pk>/', views.updateProduct, name='updateProduct'),
	path('view_ordered_item/', views.OrderItemView, name = 'view_ordered_item'),
	path('view_order/', views.OrderView, name = 'view_order'),
	path('deleteProduct/<int:pk>/', views.deleteProduct, name='deleteProduct'),
	path('search/', views.searchBar, name='search'),
	path('product/<int:pk>/', views.productDetail, name='product_details'),
	path('ViewCategory/', views.CategoryView, name = 'ViewCategory'),
	path('updateCategory/<int:pk>/', views.updateCategory, name='updateCategory'),
	path('deleteCategory/<int:pk>/', views.deleteCategory, name='deleteCategory'),
	
]