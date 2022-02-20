from django.urls import path
from .views import basket_add, basket_remove, basket_edit

app_name = 'basketapp'

urlpatterns = [
    path('add/<int:pk>/', basket_add, name='basket_add'),
    path('remove/<int:pk>)/', basket_remove, name='basket_remove'),
    path('edit/<int:pk>/<int:quantity>/', basket_edit, name='basket_edit')
]
