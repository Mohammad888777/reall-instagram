from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from two_factor.urls import urlpatterns as tf_urls


urlpatterns = [

    path('admin/', admin.site.urls),
    path("posts/",include("posts.urls")),

    path("",include("profiles.urls")),
    path('accounts/', include(tf_urls)),
    path('users/', include("accounts.urls")),
    path('comments/', include("comments.urls")),
    path('notifications/', include("notifications.urls")),


]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

