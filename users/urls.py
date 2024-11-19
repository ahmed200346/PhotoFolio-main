from django.urls import path
from .views import Register, UserDetails, UpdateView, CustomLogoutView, DetailView, Login, HomeView, UserUpdateView, \
    DeleteUser, AboutView

urlpatterns = [
    path('details/<int:pk>/', UserDetails.as_view(), name='user_details'),
    path('signup/', Register.as_view(), name='signup'),
    path('', Login.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('logout/', CustomLogoutView.as_view(), name='logout'), 
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', DeleteUser.as_view(), name='delete_user'),  
]