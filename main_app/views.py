from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Trick, Park
from .forms import TrainingForm

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
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def tricks_index(request):
    tricks=Trick.objects.all()
    return render(request, 'tricks/index.html', { 'tricks': tricks })

def tricks_detail(request, trick_id):
    trick=Trick.objects.get(id=trick_id)
    parks_trick_doesnt_have=Park.objects.exclude(id__in=trick.parks.all().values_list('id'))
    # Instantiate a Training Form
    training_form=TrainingForm()
    return render(request, 'tricks/detail.html', { 
        'trick': trick,
        'training_form': training_form,
        'parks': parks_trick_doesnt_have,
    })

def add_training(request, trick_id):
    # Create an instance of the TrainingForm
    form=TrainingForm(request.POST)
    # Validate the form
    if form.is_valid():
        new_training=form.save(commit=False)
        new_training.trick_id=trick_id
        new_training.save()
    return redirect('detail', trick_id=trick_id)

class TrickCreate(CreateView):
    model=Trick
    fields='__all__'
    success_url='/tricks/'

class TrickUpdate(UpdateView):
    model=Trick
    fields='__all__'

class TrickDelete(DeleteView):
    model=Trick
    success_url='/tricks/'


class ParkList(ListView):
  model = Park

class ParkDetail(DetailView):
  model = Park

class ParkCreate(CreateView):
  model = Park
  fields = '__all__'

class ParkUpdate(UpdateView):
  model = Park
  fields = ['name', 'location']

class ParkDelete(DeleteView):
  model = Park
  success_url = '/parks/'

def assoc_park(request, trick_id, park_id):
  # Note that you can pass a toy's id instead of the whole object
  Trick.objects.get(id=trick_id).parks.add(park_id)
  return redirect('detail', trick_id=trick_id)