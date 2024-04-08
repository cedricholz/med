from rest_framework.routers import DefaultRouter

from site_configuration.viewsets.site_configuration import StaffSiteConfigurationViewSet, SiteConfigurationViewSet

router = DefaultRouter()

router.register(r'site-configuration', SiteConfigurationViewSet, basename='site-configuration')
router.register(r'staff-site-configuration', StaffSiteConfigurationViewSet, basename='staff-site-configuration')
