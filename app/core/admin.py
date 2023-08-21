from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(MainTask)
class MainTaskAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(FullName)
class FullNameAdmin(admin.ModelAdmin):
    list_display = ('full_name',)

