from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete

urlpatterns = [
    path('', TaskList.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', TaskUpdate.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDelete.as_view(), name='task-delete'),
    path('tasks/create/', TaskCreate.as_view(), name='task-create'),
]
