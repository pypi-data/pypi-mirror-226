from netbox.api.routers import NetBoxRouter
from . import views


app_name = 'netbox_sync_status'

router = NetBoxRouter()
router.register('sync-status', views.SyncStatusViewSet)
router.register('sync-system', views.SyncSystemViewSet)

urlpatterns = router.urls


