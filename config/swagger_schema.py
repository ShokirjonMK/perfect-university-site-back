from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAdminUser

info = openapi.Info(title="TPU api", default_version="v1")

schema_view = get_schema_view(
    info=info,
    public=True,
    permission_classes=(IsAdminUser,),
)
