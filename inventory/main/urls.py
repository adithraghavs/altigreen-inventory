from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('table/<str:table_name>/', views.TableView.as_view(), name='table'),
    path('search/<str:table_name>/', views.search, name='search'),
    path('import_csv/<str:table_name>/', views.import_csv, name='import_csv'),
    path('export_to_csv/<str:table_name>/', views.export_to_csv, name='export_to_csv'),
    path('add_new/<str:table_name>/', views.add_new, name='add_new'),
    path('delete/<str:table_name>/<int:pk>/', views.delete, name='delete'),
    path('update_object/<str:table_name>/<int:pk>/', views.update_object, name='update_object'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('log_out/', views.log_out, name='log_out')
]