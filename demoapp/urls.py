from django.urls import path,include
from demoapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name="home"),
    path('about',views.about, name="about"),
    path('summary',views.summary, name="summary"),
    path('testdrive',views.testdrive),
    path('testdrive/<selected>',views.testdrive),
    path('incident',views.incident, name="incident"),
    path('edit/<to_edit>',views.edit),
    path('delete/<to_delete>',views.delete),
    path('log/new',views.driver_input),
    path('log/show',views.show_log),
    path('log/edit/<log_id>',views.edit_log),
    path('log/delete/<log_id>',views.delete_log),
    path("", include("django.contrib.auth.urls")) # /login /logout
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
