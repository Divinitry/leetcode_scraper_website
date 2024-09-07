from django.contrib import admin
from django.urls import path, include
from leetscraper.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leetscraper/', include('leetscraper.urls')),
    path('leetscraper/user/register/', CreateUserView.as_view(), name = "register"),
    path('leetscraper/token/', TokenObtainPairView.as_view(), name = "get_token"),
    path('leetscraper/token/refresh/', TokenRefreshView.as_view(), name = "refresh"),
    path('leetscraper-auth/', include('rest_framework.urls')),
]
