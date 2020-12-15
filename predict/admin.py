from django.contrib import admin
from .models import Report
# Register your models here.


admin.site.register(Report)
# class TodoAdmin(admin.ModelAdmin):
#     readonly_fields = ('created',)
#
# admin.site.register(Todo, TodoAdmin)
