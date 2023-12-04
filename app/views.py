from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from scipy.optimize import fsolve
from rest_framework.decorators import api_view
from app.models import Trilateration

from app.serializers import TrilaterationSerializer



# Create your views here.
@api_view(['GET'])
def getData(request):
    app = Trilateration.objects.all()
    serializer = TrilaterationSerializer(app, many=True)
    return JsonResponse(serializer.data,safe=False)



@api_view(['POST'])
def postData(request):
    serializer = TrilaterationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        result_data = CalculateFunction(serializer.data)
        return JsonResponse(result_data)
    return JsonResponse(serializer.errors)

def CalculateFunction(data):
    # Extract data from the provided dictionary
    lat1, lon1 = float(data['lat1']), float(data['lon1'])
    lat2, lon2 = float(data['lat2']), float(data['lon2'])
    lat3, lon3 = float(data['lat3']), float(data['lon3'])
    d1, d2, d3 = float(data['d1']), float(data['d2']), float(data['d3'])

    # Convert latitude and longitude to Cartesian coordinates
    def to_cartesian(latitude, longitude):
        R = 6371  # Earth's mean radius in kilometers
        x = R * np.cos(np.radians(latitude)) * np.cos(np.radians(longitude))
        y = R * np.cos(np.radians(latitude)) * np.sin(np.radians(longitude))
        z = R * np.sin(np.radians(latitude))
        return x, y, z

    x1, y1, z1 = to_cartesian(lat1, lon1)
    x2, y2, z2 = to_cartesian(lat2, lon2)
    x3, y3, z3 = to_cartesian(lat3, lon3)

    # Define the trilateration equations
    def equations(vars):
        x, y, z = vars
        eq1 = (x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2 - d1 ** 2
        eq2 = (x - x2) ** 2 + (y - y2) ** 2 + (z - z2) ** 2 - d2 ** 2
        eq3 = (x - x3) ** 2 + (y - y3) ** 2 + (z - z3) ** 2 - d3 ** 2
        return [eq1, eq2, eq3]

    # Initial guess for the solution
    initial_guess = [0, 0, 0]

    # Solve the equations numerically
    result = fsolve(equations, initial_guess, xtol=1e-12)

    # Convert Cartesian coordinates back to latitude and longitude
    R = 6371  # Earth's mean radius in kilometers
    rho = np.sqrt(result[0] ** 2 + result[1] ** 2)
    lat = np.arctan2(result[2], rho)
    lon = np.arctan2(result[1], result[0])

    # Convert latitude and longitude to degrees
    lat_deg = np.degrees(lat)
    lon_deg = np.degrees(lon)

    # Construct the response data
    response_data = {
        'result': f"Coordinates for point D (latitude, longitude): {lat_deg}, {lon_deg}",
        'x1': x1, 'y1': y1, 'z1': z1,
        'x2': x2, 'y2': y2, 'z2': z2,
        'x3': x3, 'y3': y3, 'z3': z3,
        'trilateration_equations_result': result.tolist(),  # Convert NumPy array to a list
    }

    return response_data
