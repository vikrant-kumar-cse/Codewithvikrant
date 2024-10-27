
from django.contrib import admin
from django.urls import path,include
from courses.views import *
from django.conf.urls.static import static
#from  Codewithvikrant.settings import MEDIA_ROOT,MEDIA_URL
from django.conf import settings
urlpatterns = [
    path('',home ,name='home'),
    path('course/<str:slug>', coursepage ,name='coursepage'),
    path('signup/', signup ,name='signup'),
    path('login/',login,name='login'),
    path('logout/',signout,name='logout'),
    path('forget-password/' , ForgetPassword , name="forget_password"),
    path('change-password/<str:token>/' , ChangePassword , name="change_password"),
    path('check-out/<str:slug>',checkout ,name='check-out'),
    path('Test/<str:slug>',Testpage,name='Testpage'),
    path('enroll/<str:slug>',enroll_course, name='enroll_course'),
    #path('enrollment-success/',enrollment_success, name='enrollment_success'),
    path('dashboard/',dashboard, name='dashboard'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)