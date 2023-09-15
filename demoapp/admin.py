from django.contrib import admin
from demoapp.models import TestLog

# Register your models here.
class TestLogAdmin(admin.ModelAdmin):
    display = ['driver', 'date', 'time','vehicle','location','label','note']
    search_fields = ['driver']

admin.site.register(TestLog,options=TestLogAdmin)