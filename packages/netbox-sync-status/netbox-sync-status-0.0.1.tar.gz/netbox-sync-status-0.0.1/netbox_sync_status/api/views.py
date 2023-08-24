from netbox.api.viewsets import NetBoxModelViewSet
from netbox_sync_status.filtersets import SyncStatusFilterSet
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from dcim.models import Device
from drf_spectacular.utils import extend_schema
from django.db.models import Prefetch


from .. import models
from .serializers import SyncStatusSerializer, SyncSystemSerializer, SyncSystemDeviceStatusSerializer


class SyncStatusViewSet(NetBoxModelViewSet):
    queryset = models.SyncStatus.objects
    serializer_class = SyncStatusSerializer
    filterset = SyncStatusFilterSet



class SyncSystemViewSet(NetBoxModelViewSet):
    queryset = models.SyncSystem.objects
    serializer_class = SyncSystemSerializer

    @extend_schema(
        responses=SyncSystemDeviceStatusSerializer(many=True), 
        request=None
    )
    @action(
        detail=True, methods=['get'],
        url_path='sync-status',
        renderer_classes=[JSONRenderer]
    )
    def render_system_sync_staus(self, request, pk):
        """
        Resolve and render the sync status of all devices
        """
        system = self.get_object()
        devices = Device.objects.prefetch_related(
            Prefetch(
                "sync_status",
                queryset=models.SyncStatus.objects.filter(system__id = system.id),
                to_attr="sync_events"
            )
        ).all()

        results = []
        for device in devices:
            if len(device.sync_events) > 0:
                results.append({
                    "device_name": device.name,
                    "status": device.sync_events[0].status
                })
            else:
                results.append({
                    "device_name": device.name,
                    "status": "not-started"
                })

        return Response(results)
