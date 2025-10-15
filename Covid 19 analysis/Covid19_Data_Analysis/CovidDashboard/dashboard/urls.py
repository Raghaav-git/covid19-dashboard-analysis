from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('compare/', views.compare, name='compare'),
    
    # API endpoints for AJAX calls
    path('api/global-time-series/', views.get_global_time_series, name='global_time_series'),
    path('api/gender-data/', views.get_gender_data, name='gender_data'),
    path('api/age-data/', views.get_age_data, name='age_data'),
    path('api/world-map-data/', views.get_world_map_data, name='world_map_data'),
    path('api/country-comparison/', views.get_country_comparison, name='country_comparison'),
    path('api/countries-list/', views.get_countries_list, name='countries_list'),
]