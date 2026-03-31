from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("apps.users.urls")),
    path('product/', include("apps.product.urls")),
    path('sotuv/', include("apps.order.urls")),
    path('customer/', include("apps.customer.urls")),
    path('shop/', include("apps.shop.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
