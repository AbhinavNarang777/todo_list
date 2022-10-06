from audioop import reverse
from http.client import HTTPResponse
import imp
from re import search
from turtle import title
from urllib.request import HTTPErrorProcessor
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

# cant access tasks without login, i.e the default path
from django.contrib.auth.mixins import LoginRequiredMixin 
# change of settings required

# to register and login a user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

#login logout
# default is logion view provided by django
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields= '__all__'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('tasks')

#for logout we just have to redirect . Check urls.py


# register user
class RegisterPage(FormView):
    # create
    template_name= 'base/register.html'
    form_class= UserCreationForm
    success_url= reverse_lazy('tasks')

    # logging in and redirect
    def form_valid(self, form):
        user= form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    # to redirect once regitsered
    def get(self , *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

#list functionality begins here
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name= "tasks" # to change name of default table

    # we want user to access their data only 
    # method to do that follows(documentation)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count() 

        search_input= self.request.GET.get('search-area') or ''
        if(search_input):
            context['tasks']= context['tasks'].filter(title__startswith=search_input)

            context['search_input']= search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name="task"
    template_name= 'base/task.html' # to change the template name form deafult to other

class TaskCreate(LoginRequiredMixin, CreateView):
    model= Task
    fields= ['title', 'description', 'complete']
    success_url= reverse_lazy('tasks')

    # a user should be able to add task in their profile only
    # the method follows(documentation)
    def form_valid(self, form) :
        form.instance.user= self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model= Task
    fields= ['title', 'description', 'complete']
    success_url= reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model= Task
    context_object_name= 'task'
    success_url= reverse_lazy('tasks')