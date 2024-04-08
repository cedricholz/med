from rest_framework.decorators import action
from rest_framework.response import Response


class ModelChoicesMixin(object):
    """
    Mixin for getting choices from models
    """

    @action(detail=False)
    def model_choices(self, request, pk=None):
        fields = request.GET.getlist("fields")

        data = {}
        for f in fields:
            data[f] = {}
            field = self.queryset.model._meta.get_field(f)
            data[f]["key_display"] = " ".join(
                [w.capitalize() for w in str(field.verbose_name).split()]
            )
            data[f]["choices"] = [
                {"key": str(c[1]), "value": str(c[0])}
                for c in field.choices
                if c[0] != ""
            ]
        return Response(data)
