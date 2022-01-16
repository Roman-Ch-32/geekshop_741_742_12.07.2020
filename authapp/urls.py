from django.urls import path

from .views import Logout, LoginListView, RegisterListView, EditListView, GoogleAuth

app_name = 'authapp'




urlpatterns = [
    path('login/', LoginListView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', RegisterListView.as_view(), name='register'),
    path('edit/', EditListView.as_view(), name='edit'),
    path("all/", GoogleAuth.as_view(), name="all"),
    path('verify/<str:email>/<str:activate_key>/', RegisterListView.verify, name='verify'),
]
