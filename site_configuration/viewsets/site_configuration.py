from django.http import HttpResponseBadRequest
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from api.sendgrid import SendgridApi
from med.logger import Log
from site_configuration.models import SiteConfiguration
from site_configuration.serializers.site_configuration import SiteConfigurationSerializer, \
    StaffSiteConfigurationSerializer
from util.aws import get_presigned_put_url


class SiteConfigurationViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
):
    queryset = SiteConfiguration.objects.all()
    serializer_class = SiteConfigurationSerializer

    def get_queryset(self):
        return super().get_queryset()


    @action(methods=["post"], detail=False)
    def get_aws_put_url(self, request, pk=None):

        try:
            content_type = request.data.get("content_type", None)

            presigned_put_url, final_url = get_presigned_put_url(
                content_type=content_type,
            )

            return Response(
                {

                    "put_url": presigned_put_url,
                    "url": final_url,
                    "storage_class": "INTELLIGENT_TIERING",
                }
            )
        except Exception as exc:
            Log.error(
                title="generate_upload_url (Code 1)",
                exc=exc,
            )
            return HttpResponseBadRequest()

    @action(methods=["post"], detail=False)
    def action_contact(self, request, pk=None):
        try:
            data = request.data
            files = data.get('files', [])
            api = SendgridApi()
            api.send_contact_email(
                name=data.get("name"),
                email=data.get("email"),
                phone=data.get("phone"),
                message_text=data.get("message"),
                files=files,
                raise_error=True
            )
            return Response(status=HTTP_204_NO_CONTENT)
        except Exception as exc:
            Log.error(
                title="action_contact (Code 1)",
                exc=exc,
            )
            body = ""
            try:
                body = str(exc.body)
            except Exception as exc:
                pass
            raise NotAcceptable()
            # return Response(status=HTTP_400_BAD_REQUEST, data={"error": str(exc), "body": body})


class StaffSiteConfigurationViewSet(
    SiteConfigurationViewSet,
):
    queryset = SiteConfiguration.objects.all()
    serializer_class = StaffSiteConfigurationSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return super().get_queryset()
