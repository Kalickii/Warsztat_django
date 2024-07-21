from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from django.views import View



class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html')

