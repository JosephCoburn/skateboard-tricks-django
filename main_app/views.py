from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Trick, Park, Photo
from .forms import TrainingForm
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'skate-tricks-js'


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

@login_required
def tricks_index(request):
    tricks=Trick.objects.filter(user=request.user)
    return render(request, 'tricks/index.html', { 'tricks': tricks })

@login_required
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

@login_required
def add_training(request, trick_id):
    # Create an instance of the TrainingForm
    form=TrainingForm(request.POST)
    # Validate the form
    if form.is_valid():
        new_training=form.save(commit=False)
        new_training.trick_id=trick_id
        new_training.save()
    return redirect('detail', trick_id=trick_id)

class TrickCreate(LoginRequiredMixin, CreateView):
    model=Trick
    # fields='__all__'
    fields=['name', 'stance', 'description', 'dial']
    success_url='/tricks/'

    def form_valid(self, form):
      # Assign the logged in user (self.request.user)
      form.instance.user = self.request.user
      # Let the CreateView do its job as usual
      return super().form_valid(form)

class TrickUpdate(LoginRequiredMixin, UpdateView):
    model=Trick
    fields='__all__'

class TrickDelete(LoginRequiredMixin, DeleteView):
    model=Trick
    success_url='/tricks/'


class ParkList(LoginRequiredMixin, ListView):
  model = Park

class ParkDetail(LoginRequiredMixin, DetailView):
  model = Park

class ParkCreate(LoginRequiredMixin, CreateView):
  model = Park
  fields = '__all__'

class ParkUpdate(LoginRequiredMixin, UpdateView):
  model = Park
  fields = ['name', 'location']

class ParkDelete(LoginRequiredMixin, DeleteView):
  model = Park
  success_url = '/parks/'

@login_required
def assoc_park(request, trick_id, park_id):
  # Note that you can pass a toy's id instead of the whole object
  Trick.objects.get(id=trick_id).parks.add(park_id)
  return redirect('detail', trick_id=trick_id)

@login_required
def unassoc_park(request, trick_id, park_id):
  # Note that you can pass a toy's id instead of the whole object
  Trick.objects.get(id=trick_id).parks.remove(park_id)
  return redirect('detail', trick_id=trick_id)

@login_required
def add_photo(request, trick_id):
    photo_file=request.FILES.get('photo-file', None)
    if photo_file:
        s3=boto3.client('s3')
        # Need a unique 'key' for S3 / needs image file extension too
        key=uuid.uuid4().hex[:6]+photo_file.name[photo_file.name.rfind('.'):]
        # In case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url=f"{S3_BASE_URL}{BUCKET}/{key}"
            # we an assign to trick_id or trick (if you have a trick object)
            photo=Photo(url=url, trick_id=trick_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', trick_id=trick_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)