from django.contrib import admin
from .models import Task, Status, Type


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'description', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'type']
    search_fields = ['summary']


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
