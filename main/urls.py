from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('browser', views.BrowserViewSet, basename='browser')
router.register('alarm_list', views.AlarmListViewSet, basename='alarm_list')
router.register('array_data', views.ArrayDataViewSet, basename='array_data')
router.register('event_index_plot', views.EventIndexPlotViewSet, basename="event_index_plot")
router.register('event_location_print', views.EventLocationPrintViewSet, basename="event_location_print")
router.register('table_list', views.TableListViewSet, basename="table_list")
router.register('x_data', views.XDataViewSet, basename="x_data")
router.register('alarm_table', views.AlarmTableViewSet, basename="alarm_table")
router.register('system_alarm', views.SystemAlarmViewSet, basename="system_alarm")
router.register('end_fiber', views.EndFiberViewSet, basename="end_fiber")


# array_data_router = routers.NestedDefaultRouter(router, 'array_data', lookup='array_data')
# array_data_router.register('files', views.download_file, basename='array-files')

urlpatterns = router.urls 