from rest_framework import serializers

from file.models import File
from util.util import get_read_only_fields


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = (
            "id",
            "url",
        )
        depth = 0
        read_only_fields = get_read_only_fields(fields, writeable_fields=())


class StaffFileSerializer(FileSerializer):
    class Meta:
        model = File
        fields = FileSerializer.Meta.fields + (

        )
        depth = 0
        read_only_fields = get_read_only_fields(
            fields, writeable_fields=()
        )
