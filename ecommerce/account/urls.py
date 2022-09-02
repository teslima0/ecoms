from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from . import views
app_name='account'
urlpatterns = [
	#Leave as empty string for base url
	#path('verify/<int:id>', views.verify),
    path('signup/', views.guest_signup_view, name="signup_guest"),
    #path('signup/guestlogin', LoginView.as_view(template_name='guestlogin.html'),name='guestlogin'),
    #path('adminlogin', LoginView.as_view(template_name='ownerlogin.html'),name='adminlogin'),
    #path('logout', LogoutView.as_view(template_name='store/store.html'),name='logout'),
    #path('register/', views.register, name = 'register'),
    path('logout_user', views.logout_user, name = 'logouts'),
    path('admin_signup/', views.store_signup_view, name="admin_signup"),

    path('update-profile', views.profileUdate, name = 'update-profile'),
    path('login_user', views.login_user, name = 'loginpage'),
]