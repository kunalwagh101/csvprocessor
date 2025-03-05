from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_view, name='upload_view'),
    path('results/', views.get_result, name='get_result'),
    path('search/', views.search_data, name='search_data'),
]
