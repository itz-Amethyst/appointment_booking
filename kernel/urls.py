from django.contrib import admin
from django.urls import path , include
from drf_spectacular.views import SpectacularAPIView , SpectacularSwaggerView



urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("auth/", include("djoser.urls")),
    path("account/" , include("core.api.routers.jwt")) ,
    # path("auth/jwt/create/", Custom.as_view()),
    path("profile/" , include("core.api.routers.profile")) ,
    path("channel/" , include("appointment_booking.api.routers.channel")),
    path("general/", include("kernel.general.routers.main")),


    # ! Docs
    path('api/schema/' , SpectacularAPIView.as_view() , name = 'schema') ,
    path('api/docs/' , SpectacularSwaggerView.as_view(url_name = 'schema') , name = 'swagger-ui') ,
]
