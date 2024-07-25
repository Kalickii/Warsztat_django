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


class AllRoomsView(View):
    def get(self, request):
        if not Room.objects.all().exists():
            message = 'No rooms available'
            return render(request, 'home.html', {'message': message})
        else:
            rooms = Room.objects.all()
            busy = False
            ctx = {'rooms': rooms, 'busy': busy}
            return render(request, 'all_room_list.html', ctx)


class RoomDeleteView(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        room.delete()
        return redirect('http://127.0.0.1:8000/room/list/')


class RoomModifyView(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        hidden_id = room_id
        ctx = {'room': room, 'hidden_id': hidden_id}
        return render(request, 'modify_room.html', ctx)

    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        projector = int(request.POST.get('projector'))
        if name and capacity > 0:
            if not Room.objects.filter(name=name).exists() or name == room.name:
                room.name = name
                room.capacity = capacity
                room.have_projector = projector
                room.save()
                return redirect('http://127.0.0.1:8000/room/list')
            else:
                message = 'Error: Room already exists'
                return render(request, 'modify_room.html', {'message': message})
        else:
            message = 'Error: Empty field or negative room capacity'
            return render(request, 'modify_room.html', {'message': message})
