
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from .views import *
from django.urls import path, include

from rest_framework import routers


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('RegisterNewUserUser/', RegisterNewUserUser,
         name='RegisterNewUserUser'),
    path('LoggedInUsersDetails/', LoggedInUsersDetails,
         name='LoggedInUsersDetails'),
    path('CreateTransaction/', CreateTransaction,
         name='CreateTransaction'),

    path('AllPendingTransaction/', AllPendingTransaction,
         name='AllPendingTransaction'),
    path('MineBlock/', MineBlock,
         name='MineBlock'),
    path('MineBlockDetails/', MineBlockDetails,
         name='MineBlockDetails'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
