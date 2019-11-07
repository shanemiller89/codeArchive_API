"""codearchiveAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
# from django.contrib import admin

from codearchiveAPIapp.views import Libraries
from codearchiveAPIapp.views import LibraryTypes
from codearchiveAPIapp.views import Archives
from codearchiveAPIapp.views import LibraryArchives
from codearchiveAPIapp.views import Articles
from codearchiveAPIapp.views import Events
from codearchiveAPIapp.views import LogTypes
from codearchiveAPIapp.views import Logs
from codearchiveAPIapp.views import LogArchives
from codearchiveAPIapp.views import RecordTypes
from codearchiveAPIapp.views import Records
from codearchiveAPIapp.views import ResourceTypes
from codearchiveAPIapp.views import Resources
from codearchiveAPIapp.views import UserViewSet, Coders
from codearchiveAPIapp.views import register_user, login_user


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'libraries', Libraries, 'library')
router.register(r'librarytype', LibraryTypes, 'librarytype')
router.register(r'archives', Archives, 'archive')
router.register(r'libraryarchives', LibraryArchives, 'libraryarchive')
router.register(r'articles', Articles, 'article')
router.register(r'events', Events, 'event')
router.register(r'logtypes', LogTypes, 'logtype')
router.register(r'logs', Logs, 'log')
router.register(r'logarchives', LogArchives, 'logarchive')
router.register(r'recordtypes', RecordTypes, 'recordtype')
router.register(r'records', Records, 'record')
router.register(r'resourcetypes', ResourceTypes, 'resourcetype')
router.register(r'resources', Resources, 'resource')
router.register(r'coders', Coders, 'coder')
router.register(r'users', UserViewSet, 'user')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^admin/', admin.site.urls),
]