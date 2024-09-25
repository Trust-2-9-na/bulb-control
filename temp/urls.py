
from django.urls import path 
from temp.views import index, SensorDataList, average_sensor_data, charts_view, relay_control, BulbControlView

urlpatterns = [
  path('', index, name='index'),  # The index view that renders sensor data in HTML
  path('api/sensor-data/', SensorDataList.as_view(), name='sensor-data-list'), 
  path('average-sensor-data/', average_sensor_data, name='average_sensor_data'),
  path('charts/', charts_view, name='charts_view'),
  path('api/relay-control/', relay_control, name='relay_control'),
  path('bulb-control/', BulbControlView.as_view(), name='bulb_control'),
]