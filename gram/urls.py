from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.home, name='home'),
    url(r'^welcome/', views.welcome, name='welcome'),
    url(r'^timeline/', views.timeline, name='timeline'),
    url(r'^search/', views.search, name='search'), 
    url(r'^post/', views.post, name='post'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^update/profile', views.update_profile, name='updateProfile'),
    url(r'^view/profiles', views.view_profiles, name='viewProfiles'),
    url(r'^user/(\d+)', views.single_user, name='user'),
    url(r'^image/(\d+)', views.single_image, name='image'),
    url(r'^update/image/(\d+)', views.update_image, name='updateImage'),
    url(r'^comment/(\d+)', views.comment, name='comment'),
    url(r'^follow/(\d+)',views.follow ,name='follow'), 
    url(r'^like/(\d+)',views.like ,name='like'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)