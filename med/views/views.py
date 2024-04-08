from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView

# Serve Single Page Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


# @csrf_exempt
# @api_view(['POST'])
# def contact(request):
#     data = request.data
#     files = data.get('files', [])
#     try:
#         SendgridApi().send_contact_email(
#             name=data.get("name"),
#             email=data.get("email"),
#             phone=data.get("phone"),
#             message_text=data.get("message"),
#             files=files,
#             raise_error=True,
#         )
#     except Exception as exc:
#         Log.error("contact", exc=exc, data=data)
#         raise exc
#     return Response(status=HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['POST'])
def refresh(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token_data = serializer.validated_data
    return Response({'token': token_data['access']})


class CookieTokenRefreshView(TokenRefreshView):
    def get_refresh(self):
        return self.request.COOKIES.get('refresh')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                'refresh': self.get_refresh(),
            }
        )

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=HTTP_200_OK)
