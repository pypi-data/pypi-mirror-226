from django.urls import path
from . import views


urlpatterns = (
    path('sync-status/', views.SyncStatusListView.as_view(), name='syncstatus_list_device'),
)