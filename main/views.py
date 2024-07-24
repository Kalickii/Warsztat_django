from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from main.models import Room

class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html')

class NewRoomView(View):
    def get(self, request):
        return render(request, 'new_room.html')

    def post(self, request):
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        projector = int(request.POST.get('projector'))
        if name and capacity > 0:
            if not Room.objects.filter(name=name).exists():
                Room.objects.create(name=name, capacity=capacity, have_projector=projector)
                return redirect('http://127.0.0.1:8000/')
            else:
                message = 'Error: Room already exists'
                return render(request, 'new_room.html', {'message': message})
        else:
            message = 'Error: Empty field or negative room capacity'
            return render(request, 'new_room.html', {'message': message})



