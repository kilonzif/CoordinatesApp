from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from scipy.optimize import fsolve
import numpy as np

class TrilaterationView(View):
    template_name = 'app_result.html'

    def post(self, request, *args, **kwargs):
        # Extract data from the POST request
        data = request.POST
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

        # Print the result
        result_str = f"Coordinates for point D (latitude, longitude): {lat_deg}, {lon_deg}"

        # Return the result in the response
        context = {
            'result': result_str,
            'x1': x1, 'y1': y1, 'z1': z1,
            'x2': x2, 'y2': y2, 'z2': z2,
            'x3': x3, 'y3': y3, 'z3': z3,
            'trilateration_equations_result': result,
        }

        return render(request, self.template_name, context)
