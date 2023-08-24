from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from ..models import SyncStatus, SyncSystem


#

#
# Regular serializers
#

class SyncStatusSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_sync_status-api:syncstatus-detail"
    )

    class Meta:
        model = SyncStatus
        fields = (
            "created", "url", "device", "system", "status", "message"
        )


class SyncSystemSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_sync_status-api:syncsystem-detail"
    )

    class Meta:
        model = SyncSystem
        fields = (
            "created", "url", "name", "description"
        )


class SyncSystemDeviceStatusSerializer(serializers.Serializer):
    device_name = serializers.CharField()
    status = serializers.CharField()
