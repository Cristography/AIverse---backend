from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('prompts.urls')),
    path('api/', include('content.urls')),
    path('api/', include('interactions.urls')),
    path('api/', include('tags.urls')),
]
