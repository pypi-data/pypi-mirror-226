import django_tables2 as tables

from netbox.tables import NetBoxTable, columns
from .models import SyncStatus


class SyncStatusListTable(NetBoxTable):
    actions = columns.ActionsColumn(
        actions=()
    )

    device = tables.Column(
        linkify=True
    )
    class Meta(NetBoxTable.Meta):
        model = SyncStatus
        title = ""
        fields = ("device", "status", "system", "message", "created")