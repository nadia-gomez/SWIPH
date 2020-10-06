from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.SW_index,name='SW_index'),
    path('basicInput/<int:pk>',views.basicInput,name='basicInput'),
    path('advancedInput/<int:pk>',views.advancedInput,name='advancedInput'),
    path('samResults/<int:pk>/<int:plt>',views.samResults,name='samResults'),
    #path('samples_creation/status/', views.mldb_status, name='mldb_status'),
    #path('async/mldb_status/',views.async_mldb_status ,name='async_mldb_status'),
    path('async/basic_classificator/',views.async_basic_classificator ,name='async_basic_classificator'),
    path('async/project_shape/nLoop',views.asyc_project_shape ,name='async_project_shape'),
    path('async/project_shape/nModBoil',views.asyc_projectshape_nModBoil ,name='async_nModBoil'),
    path('check_PT/',views.check_PT ,name='check_PT'),
]