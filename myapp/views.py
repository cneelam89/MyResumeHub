from django.shortcuts import render, HttpResponseRedirect
from .forms import ResumeForm
from .models import Resume
from django.views import View
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group


class HomeView(View):
 def get(self, request):
  form = ResumeForm()
  user = request.user
  gps = user.groups.all()
  # candidates = Resume.objects.filter( user=request.user)
  current_user_groups = request.user.groups.values_list("name", flat=True)
  if "Author" in current_user_groups:
    candidates = Resume.objects.filter( user=request.user)
  else:
    candidates = Resume.objects.all()
  print(current_user_groups)
  return render(request, 'myapp/home.html', { 'candidates':candidates, 'form':form})

 def post(self, request):
  form = ResumeForm(request.POST, request.FILES)
  if form.is_valid():
   name=form.cleaned_data["name"]
   dob=form.cleaned_data["dob"]
   gender=form.cleaned_data["gender"]
   locality=form.cleaned_data["locality"]
   city=form.cleaned_data["city"]
   pin=form.cleaned_data["pin"]
   state=form.cleaned_data["state"]
   mobile=form.cleaned_data["mobile"]
   email=form.cleaned_data["email"]
   job_city=form.cleaned_data["job_city"]
   profile_image=form.cleaned_data["profile_image"]
   my_file=form.cleaned_data["my_file"]
   user = request.user
   state=form.cleaned_data["state"]
   state=form.cleaned_data["state"]
   pst = Resume(name=name, dob=dob,gender=gender,locality=locality,city=city,pin=pin,state=state,mobile=mobile,email=email,job_city=job_city,profile_image=profile_image,my_file=my_file,user=user)
   pst.save()
   return render(request, 'myapp/home.html', {'form':form})

# class CandidateView(View):
#  def get(self, request, pk):  
#   candidate = Resume.objects.get(pk=pk)
#   return render(request, 'myapp/candidate.html', {'candidate':candidate})

def CandidateView(request,id):
    candidate = Resume.objects.get(pk=id)
    return render(request, 'myapp/candidate.html', {'candidate':candidate})
 

def user_signup(request):
  if not request.user.is_authenticated:
    if request.method == "POST":
      form = SignUpForm(request.POST)
      if form.is_valid():
        messages.success(request, 'Congratulations!! You have become an Author.')
        messages.info(request, 'hi.')
        user = form.save()
        group = Group.objects.get(name='Author')
        user.groups.add(group)
        return HttpResponseRedirect('/login/')
    else:
      form = SignUpForm()
      return render(request, 'myapp/signup.html', {'form':form})
  else:
    return HttpResponseRedirect('/home/')

# Login
def user_login(request):
 if not request.user.is_authenticated:
  if request.method == "POST":
   form = LoginForm(request=request, data=request.POST)
   if form.is_valid():
    uname = form.cleaned_data['username']
    upass = form.cleaned_data['password']
    user = authenticate(username=uname, password=upass)
    if user is not None:
     login(request, user)
     messages.success(request, 'Logged in Successfully !!')
     return HttpResponseRedirect('/home/')
  else:
   form = LoginForm()
  return render(request, 'myapp/login.html', {'form':form})
 else:
  return HttpResponseRedirect('/home/')
 
def user_logout(request):
 logout(request)
 return HttpResponseRedirect('/')


# Update/Edit Post
def update_data(request, id):
  if request.user.is_authenticated:
    if request.method == 'POST':
      pi = Resume.objects.get(pk=id)
      form = ResumeForm(request.POST, instance=pi)
      if form.is_valid():
        form.save()
    else:
      pi = Resume.objects.get(pk=id)
      form = ResumeForm(instance=pi)
    return render(request, 'myapp/updatedata.html', {'form':form})
  else:
    return HttpResponseRedirect('/login/')

# Delete Post
def delete_post(request, id):
  if request.user.is_authenticated:
    if request.method == 'POST':
      pi = Resume.objects.get(pk=id)
      pi.delete()
      return HttpResponseRedirect('/home/')
  else:
    return HttpResponseRedirect('/login/')


