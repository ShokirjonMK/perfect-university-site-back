from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from admin_panel.model import static
from admin_panel.model import menu
from . import serializers


class StaticView(viewsets.ModelViewSet):
    queryset = static.StaticPage.objects.filter(active=True)
    serializer_class = serializers.StaticSerializer
    pagination_class = None
    http_method_names = ['get']
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.views += 1
        instance.save()

        serializer = self.serializer_class
        menu_serializer = serializers.StaticMenuSerializer
        page_menu = menu.Menu.objects.filter(url=instance.slug)
        if page_menu.exists():
            page_menu = page_menu.last()
            parent_menu = page_menu.parent
            result = menu.Menu.objects.filter(parent=parent_menu)
            payload = {
                'page': serializer(instance).data,
            }
            if page_menu:
                payload['title'] = parent_menu.title
            if result:
                payload['menu'] = menu_serializer(result, many=True).data

        else:
            parent_menu = menu.Menu.objects.filter(parent__isnull=False).order_by('-order').last()
            result = menu.Menu.objects.filter(parent=parent_menu)
            payload = {
                'title': parent_menu.title,
                'menu': menu_serializer(result, many=True).data,
                'page': serializer(instance).data,
            }
        return Response(payload, status=status.HTTP_200_OK)
