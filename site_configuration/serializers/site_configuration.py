from rest_framework import serializers

from site_configuration.models import SiteConfiguration
from util.util import get_read_only_fields


class SiteConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = (
            "id",

        )
        depth = 0
        read_only_fields = get_read_only_fields(fields, writeable_fields=())


class StaffSiteConfigurationSerializer(SiteConfigurationSerializer):
    class Meta:
        model = SiteConfiguration
        fields = SiteConfigurationSerializer.Meta.fields + (

        )
        depth = 0
        read_only_fields = get_read_only_fields(fields, writeable_fields=())
