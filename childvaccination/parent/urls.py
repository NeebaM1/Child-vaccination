"""
URL configuration for childvaccination project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from parent import views
app_name='parent'

urlpatterns = [
    path('add_info/<int:id>',views.add_info,name='add_info'),
    path('view_details/<int:id>',views.view_details,name='view_details'),
    path('my_profile/<int:id>',views.my_profile,name='my_profile'),
    path('edit_profile/<int:id>',views.edit_profile,name='edit_profile'),
    path('editchild_details/<int:id>',views.editchild_details,name='editchild_details'),
    path('delete_details/<int:id>',views.delete_details,name='delete_details'),
    path('vaccine_details/<int:id>', views.vaccine_details, name='vaccine_details'),
    path('add_vaccine_date/<int:id>', views.add_vaccine_date, name='add_vaccine_date'),
    path('book_appoinment/<int:child_id>',views.book_appoinment,name='book_appoinment'),
    path('appoinmentdetail',views.appoinmentdetail,name='appoinmentdetail'),
   

]


