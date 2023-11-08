from django.urls import path,include
from demoapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index),
    path('about',views.about),
    path('summary',views.summary),
    path('testdrive',views.testdrive),
    path('testdrive/<selected>',views.testdrive),
    path('incident',views.incident),
    # path('incident/<select_operation>/<selected>',views.incident2),
    path('edit/<to_edit>',views.edit),
    path('delete/<to_delete>',views.delete),
    path('new-log',views.driver_input),
    path('show-log',views.show_log),
    path('edit-log/<log_id>',views.edit_log),
    path('delete-log/<log_id>',views.delete_log),
    path('test',views.test),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
