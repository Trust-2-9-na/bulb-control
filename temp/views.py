from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SensorData, BulbControl
from .serializers import SensorDataSerializer
from rest_framework import status
from django.utils import timezone
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
import json
from django.views import View
from .models import BulbControl

# Global variable to store relay state
relay_state = "off"  # Initially, the relay is off

# API View for Relay Control
@csrf_exempt
def relay_control(request):
    if request.method == "GET":
        # Fetch the most recent bulb control status
        try:
            bulb_control = BulbControl.objects.latest('timestamp')  # Get the most recent record
            return JsonResponse({"relay": bulb_control.status}, status=200)
        except BulbControl.DoesNotExist:
            return JsonResponse({"error": "No bulb control data found"}, status=404)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            new_state = data.get("relay").upper()  # Ensure state is in uppercase

            if new_state in ["ON", "OFF"]:
                # Update the database with the new status
                BulbControl.objects.create(status=new_state)  # Create a new BulbControl record
                return JsonResponse({"relay": new_state}, status=200)
            else:
                return JsonResponse({"error": "Invalid relay state"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Bad request"}, status=400)
        


def index(request):
    # Retrieve all sensor data
    sensor_data = SensorData.objects.all()
    
    # Serialize the sensor data
    serializer = SensorDataSerializer(sensor_data, many=True)
    sensor_data_json = json.dumps(serializer.data)

    # Pass the serialized sensor data to the template
    return render(request, 'temp/index.html', {
        'sensor_data_json': sensor_data_json
    })

class BulbControlView(View):
    def get(self, request, *args, **kwargs):
        # Render the HTML page
        return render(request, 'temp/bulb_control.html')

    def post(self, request, *args, **kwargs):
        # Retrieve the code or command from the POST data
        command = request.POST.get('code') or request.POST.get('command')
        
        # Determine the status based on the command or code received
        if command in ['SWITCH_ON', 'ON']:
            status = 'ON'
        elif command in ['SWITCH_OFF', 'OFF']:
            status = 'OFF'
        else:
            return JsonResponse({'error': 'Invalid command or code'}, status=400)

        # Create a new BulbControl instance and save it to the database
        bulb_control = BulbControl(status=status)
        bulb_control.save()

        # Return a success response
        return JsonResponse({'message': f'Bulb turned {status}', 'status': status}, status=200)


        

def charts_view(request):
    sensor_data = SensorData.objects.all()
    serializer = SensorDataSerializer(sensor_data, many=True)
    sensor_data_json = json.dumps(serializer.data)
    return render(request, 'temp/charts.html', {'sensor_data_json': sensor_data_json})

# APIView for handling GET and POST requests for SensorData
class SensorDataList(APIView):
    def get(self, request, *args, **kwargs):
        sensor_data = SensorData.objects.all()
        serializer = SensorDataSerializer(sensor_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for calculating and displaying the average sensor data over the last hour
def average_sensor_data(request):
    try:
        # Get the current time
        now = timezone.now()

        # Calculate one hour ago
        one_hour_ago = now - timezone.timedelta(hours=1)

        # Query for sensor data in the last hour
        recent_data = SensorData.objects.filter(timestamp__gte=one_hour_ago)

        # Calculate average temperature and humidity
        averages = recent_data.aggregate(
            avg_temperature=Avg('temperature'),
            avg_humidity=Avg('humidity')
        )

        # Extract average values
        avg_temperature = averages['avg_temperature']
        avg_humidity = averages['avg_humidity']

        # Format to two decimal points
        avg_temperature = round(avg_temperature, 2) if avg_temperature is not None else 0
        avg_humidity = round(avg_humidity, 2) if avg_humidity is not None else 0

        context = {
            'avg_temperature': avg_temperature,
            'avg_humidity': avg_humidity
        }

        return render(request, 'temp/average.html', context)

    except Exception as e:
        # Handle any exceptions and provide a meaningful response
        return render(request, 'temp/error.html', {'error_message': str(e)})
