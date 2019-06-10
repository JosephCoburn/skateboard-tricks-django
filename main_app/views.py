from django.shortcuts import render
from django.http import HttpResponse
from .models import Trick

# class Trick:
#     def __init__(self, name, stance, description, dial):
#         self.name = name
#         self.stance = stance
#         self.description = description
#         self.dial = dial

# tricks = [
#     Trick('Ollie', 'Regular', 'Jump with board by popping tail and sliding front foot', 85),
#     Trick('Shuv-It', 'Regular', 'Spin board 180° on ground', 75),
#     Trick('Pop Shuv-It', 'Regular', 'Pop tail and spin board 180° in air', 60),
#     Trick('Kickflip', 'Regular', 'Board does barrel roll in air by popping tail and flicking front foot off side of nose', 40),
# ]

# Create your views here.
def home(request):
    return HttpResponse('<h1>as</h1>')

def about(request):
    return render(request, 'about.html')

def tricks_index(request):
    tricks=Trick.objects.all()
    return render(request, 'tricks/index.html', { 'tricks': tricks })

def tricks_detail(request, trick_id):
    trick=Trick.objects.get(id=trick_id)
    return render(request, 'tricks/detail.html', { 'trick': trick })