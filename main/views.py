from django.shortcuts import render, redirect
from django.views import View
from django.utils.timezone import localdate

from datetime import date

from main.models import Room, Booking


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
            bookings = Booking.objects.all()
            room_status = {}

            for room in rooms:
                room_busy = 'No'
                for booking in bookings:
                    if Booking.objects.filter(room=room, date=localdate()).exists():
                        room_busy = 'Yes'
                        break
                room_status[room.id] = room_busy

            rooms_with_status = []
            for room in rooms:
                rooms_with_status.append({
                    'id': room.id,
                    'name': room.name,
                    'capacity': room.capacity,
                    'have_projector': room.have_projector,
                    'status': room_status[room.id]
                })

            ctx = {'rooms': rooms_with_status}
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


class RoomBookView(View):
    def get(self, request, book_room_id):
        room = Room.objects.get(pk=book_room_id)
        return render(request, 'book_room.html', {"room": room})

    def post(self, request, book_room_id):
        room = Room.objects.get(pk=book_room_id)
        book_date = request.POST.get('date')
        comment = request.POST.get('comment')

        if Booking.objects.filter(room=room, date=book_date):
            message = "That room is already booked!"
            ctx = {"room": room, "message": message}
            return render(request, 'book_room.html', ctx)
        if book_date < str(date.today()):
            message = "That date is from the past!"
            ctx = {"room": room, "message": message}
            return render(request, 'book_room.html', ctx)

        Booking.objects.create(room=room, date=book_date, comment=comment)
        return redirect("http://127.0.0.1:8000/room/list")

#cos  nie dzialaxd strona po kliknieciu Book sie ładuje caly czas i nicsie nie dzieje nie  zapisuje w bazie danych