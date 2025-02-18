from django.contrib import admin
from . import models
from datetime import datetime, timedelta, time


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_name', 'format', 'active', 'cr_on']
    list_editable = ['active']
    list_per_page = 10
    list_filter = ['format', 'active', 'cr_on']
    ordering = ['-cr_on']
    readonly_fields = ['cr_on', 'up_on']
    search_fields = ['id', 'file_name', 'format']


@admin.register(models.Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['id', 'word_value', 'active', 'cr_on']
    list_editable = ['active']
    list_per_page = 10
    list_filter = ['active', 'cr_on']
    ordering = ['-cr_on']
    readonly_fields = ['cr_on', 'up_on']
    search_fields = ['id', 'word_value']


@admin.register(models.WordsInFiles)
class WordsInFilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'word', 'count', 'active', 'cr_on']
    list_editable = ['active']
    list_per_page = 20
    list_filter = ['count', 'active', 'cr_on']
    ordering = ['-cr_on']
    readonly_fields = ['cr_on', 'up_on']
    search_fields = ['id', 'file', 'word', 'count']


