from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('videos.urls')),
    path('v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]