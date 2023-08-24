from netbox.views import generic
from netbox_sync_status.filtersets import SyncStatusFilterForm, SyncStatusFilterSet
from .tables import SyncStatusListTable
from .models import SyncStatus


class SyncStatusListView(generic.ObjectListView):
    queryset = SyncStatus.objects.order_by("-id")
    table = SyncStatusListTable
    filterset = SyncStatusFilterSet
    filterset_form = SyncStatusFilterForm
    actions = ("export")
    template_name = "netbox_sync_status/sync_status_list.html"
