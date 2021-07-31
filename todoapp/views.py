from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView,UpdateView,DeleteView
from django.views.generic import View

from .models import Tasks

from django.contrib.auth.views import LoginView, redirect_to_login

from .forms import UserForm
from .forms import SignUpForm
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from todoapp.tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.core.mail import EmailMessage

from django import http
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django import forms
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib import messages


from django.contrib.auth.decorators import login_required
# from django.http import Http404

# Create your views here.



class UserLoginView(LoginView):
    template_name='tasks/login.html'
    redirect_authenticated_user=True
    success_url=reverse_lazy('index')

    # def get_success_url(self):
    #     return reverse_lazy('index')

class SignUpView(FormView):
    form_class=UserForm
    template_name='tasks/signup.html'
    # success_url=reverse_lazy('index')
    # redirect_to_login=True

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        # if user is not None:
        #     login(self.request,user)
        # return super().form_valid(form)
        
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            current_site=get_current_site(request)
            subject='Activate My Manager Account'
            message=render_to_string(
                'tasks/confirm_email.html',{
                    'user':user,
                    'domain':current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    

        return render(request, self.template_name, {'form': form})

            


    
    

class HomePage(TemplateView):
    template_name='tasks/index.html'
    
class ViewAllTasks(LoginRequiredMixin, ListView):
    model=Tasks
    context_object_name="all_tasks"
    template_name='tasks/tasks.html'
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['all_tasks']=context['all_tasks'].filter(user=self.request.user)
        context['count']=context['all_tasks'].filter(completed=False).count()

        search_task=self.request.GET.get('search_item')
        if search_task:
            context['all_tasks']=context['all_tasks'].filter(task_title__icontains=search_task)
        context['search_task']=search_task
        return context

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')

class Viewtask(LoginRequiredMixin, DetailView):
    model=Tasks
    context_object_name='task'
    template_name='tasks/view_task.html'

class AddTask(LoginRequiredMixin, CreateView):
    model=Tasks
    fields=['task_title','description','completed']
    template_name='tasks/addtask.html'
    success_url=reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(AddTask,self).form_valid(form)

class UpdateTask(LoginRequiredMixin, UpdateView):
    model=Tasks
    fields="__all__"
    template_name='tasks/addtask.html'
    success_url=reverse_lazy("index")

class DeleteTask(LoginRequiredMixin, DeleteView):
    model=Tasks
    context_object_name='task'
    template_name='tasks/delete_task.html'
    success_url=reverse_lazy("index")



# def login_page(request):
#     if request.method=="POST":
#         usern=request.POST["username"]
#         passw=request.POST["password"]
#         user=authenticate(request,username=usern,password=passw)
#         if user is not None:
#             login(request,user)
#             return HttpResponseRedirect(reverse('index'))
#         else:
#             return render(request,'tasks/login.html',{
#                 "message":"Invalid Username or Password"
#             })
#     return render(request,"tasks/login.html")


# def logout_page(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('login'))

# def signup(request):
#     if request.method=="POST":
#         user_form =UserForm(request.POST)
#         if user_form.is_valid():
#             user_form.save()
#             messages.success(request,'Account created successfully')
#             return HttpResponseRedirect(reverse('login'))            
#     else:
#         user_form = UserForm()
#     return render(request,'tasks/signup.html',{
#             'form':user_form
#         })


# def my_tasks(request,):
#     k=request.session.get(Tasks.objects)

    
#     # if "list_of_tasks" not in request.session:
#     #     request.session["list_of_tasks"]=[]
#     return render(request,'tasks/tasks.html',{
#         "all_tasks":k
#     })


# def addTask(request):
#     user=User.get_username
#     if request.user.is_authenticated:
#         if request.method=="POST":
#             form_data=NewTask(request.POST)
#             if form_data.is_valid():
                
#                 Tasks.objects.create(
#                 task=request.POST.get("task"),
#                 priority=request.POST.get("priority"),
#                 duration=request.POST.get("duration")

#             )
#                 return HttpResponseRedirect(reverse("index"))
#             else:
#                 return render(request,"tasks/addtask.html",{"form":form_data})
        
#         return render(request,"tasks/addtask.html",{
#                 "form":NewTask()
#             })
#     else:
#         return render(request,"tasks/login.html",{
#             "message":"You have to be logged in to add a task"
#         })    


