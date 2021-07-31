from django.urls import path
from . import views
from .views import ViewAllTasks,Viewtask,HomePage,AddTask,UpdateTask,DeleteTask,UserLoginView,SignUpView,ActivateAccount
from django.contrib.auth.views import LogoutView
urlpatterns=[
    path('', HomePage.as_view(),name='home'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('signup/',SignUpView.as_view(),name='signup'),
    path('mytasks/',ViewAllTasks.as_view(),name="index"),
    path('details/<int:pk>/',Viewtask.as_view(),name='task_detail'),
    path('addtask/', AddTask.as_view(), name="addtask"),
    path('update/<int:pk>/',UpdateTask.as_view(),name='update_task'),
    path('delete/<int:pk>/',DeleteTask.as_view(),name='delete_task'),



   
]