from django.urls import path
from .views.task_views import IndexView, TaskView, TaskAdd, TaskUpdate, TaskDelete

app_name = 'tracker_app'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('task/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('task/add/', TaskAdd.as_view(), name='task_add'),
    path('task/<int:pk>/update/', TaskUpdate.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete')
]