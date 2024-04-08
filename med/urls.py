from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.urls import re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from med.views.views import index_view
from router.router import router


def health_check(request):
    return HttpResponse("OK")


urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain")
    ),
    path(
        "sitemap.xml",
        TemplateView.as_view(template_name="sitemap.xml", content_type="text/plain")
    ),
    # url(r'^sitemap.xml$', serve, {'path': 'sitemap.xml', 'document_root': settings.STATIC_ROOT}),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("admin/", admin.site.urls),
    # path('api/contact/', contact, name='contact'),
    # path('redirects/cart_checkout_success/', cart_checkout_success, name='cart_checkout_success'),
    # path('webhooks/dreamship_webhook/', dreamship_webhook, name='dreamship_webhook'),
    # path('webhooks/gmail_webhook/', gmail_webhook, name='gmail_webhook'),
    # path('redirects/cart_checkout_cancel/', cart_checkout_cancel, name='cart_checkout_cancel'),
    # path('api/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    # path('api/stats/', StatsViewSet.as_view({'get': 'get'}), name='stats'),
    path('health_check', health_check, name='health_check'),
    path('health_check/', health_check, name='health_check'),
    re_path(r'^.*$', index_view, name='index'),
]
