from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'due_date', 'owner')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'tags')