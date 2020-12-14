from django.contrib import admin
from .models import Report
# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ('name',)

admin.site.register(Report, ReportAdmin)
# class TodoAdmin(admin.ModelAdmin):
#     readonly_fields = ('created',)
#
# admin.site.register(Todo, TodoAdmin)
