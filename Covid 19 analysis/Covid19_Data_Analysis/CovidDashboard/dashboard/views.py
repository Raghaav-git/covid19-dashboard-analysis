from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Avg, Q
from django.core.serializers.json import DjangoJSONEncoder
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from datetime import datetime
from .models import CovidData


def home(request):
    """Home page with global COVID graphs and world map"""
    context = {
        'title': 'COVID-19 Global Dashboard',
        'page': 'home'
    }
    return render(request, 'dashboard/home.html', context)


def compare(request):
    """Compare page with side-by-side animated graphs"""
    context = {
        'title': 'COVID-19 Compare Dashboard',
        'page': 'compare'
    }
    return render(request, 'dashboard/compare.html', context)


def get_global_time_series(request):
    """API endpoint for global time series data"""
    metric = request.GET.get('metric', 'cases')
    country = request.GET.get('country', '')
    
    # Get aggregated data by date, optionally filtered by country
    queryset = CovidData.objects.all()
    if country:
        queryset = queryset.filter(country=country)
    
    queryset = queryset.values('date').annotate(
        total_cases=Sum('cases'),
        total_deaths=Sum('deaths'),
        total_vaccinations=Sum('vaccinations')
    ).order_by('date')
    
    dates = []
    values = []
    
    for item in queryset:
        dates.append(item['date'].strftime('%Y-%m-%d'))
        if metric == 'cases':
            values.append(item['total_cases'])
        elif metric == 'deaths':
            values.append(item['total_deaths'])
        elif metric == 'vaccinations':
            values.append(item['total_vaccinations'])
    
    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines+markers',
        name=f'Global {metric.title()}',
        line=dict(width=3),
        marker=dict(size=6)
    ))
    
    title_prefix = f'{country} COVID-19' if country else 'Global COVID-19'
    fig.update_layout(
        title=f'{title_prefix} {metric.title()} Over Time',
        xaxis_title='Date',
        yaxis_title=f'Total {metric.title()}',
        template='plotly_white',
        height=400,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return JsonResponse({
        'graph': fig.to_json(),
        'data': list(zip(dates, values))
    })


def get_gender_data(request):
    """API endpoint for gender-wise data"""
    metric = request.GET.get('metric', 'cases')
    country = request.GET.get('country', '')
    
    # Get data by gender, optionally filtered by country
    male_queryset = CovidData.objects.filter(sex='M')
    female_queryset = CovidData.objects.filter(sex='F')
    
    if country:
        male_queryset = male_queryset.filter(country=country)
        female_queryset = female_queryset.filter(country=country)
    
    male_data = male_queryset.aggregate(
        total_cases=Sum('cases'),
        total_deaths=Sum('deaths'),
        total_vaccinations=Sum('vaccinations')
    )
    
    female_data = female_queryset.aggregate(
        total_cases=Sum('cases'),
        total_deaths=Sum('deaths'),
        total_vaccinations=Sum('vaccinations')
    )
    
    # Prepare data for chart
    if metric == 'cases':
        male_value = male_data['total_cases'] or 0
        female_value = female_data['total_cases'] or 0
    elif metric == 'deaths':
        male_value = male_data['total_deaths'] or 0
        female_value = female_data['total_deaths'] or 0
    elif metric == 'vaccinations':
        male_value = male_data['total_vaccinations'] or 0
        female_value = female_data['total_vaccinations'] or 0
    
    # Create Plotly pie chart
    fig = go.Figure(data=[go.Pie(
        labels=['Male', 'Female'],
        values=[male_value, female_value],
        hole=0.3,
        marker_colors=['#3498db', '#e74c3c']
    )])
    
    title_prefix = f'{country} Gender Distribution' if country else 'Gender Distribution'
    fig.update_layout(
        title=f'{title_prefix} - {metric.title()}',
        template='plotly_white',
        height=400,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return JsonResponse({
        'graph': fig.to_json(),
        'data': {
            'male': male_value,
            'female': female_value
        }
    })


def get_age_data(request):
    """API endpoint for age-wise data"""
    metric = request.GET.get('metric', 'cases')
    country = request.GET.get('country', '')
    
    # Create age groups
    age_groups = [
        (0, 20, '0-20'),
        (21, 40, '21-40'),
        (41, 60, '41-60'),
        (61, 80, '61-80'),
        (81, 120, '81+')
    ]
    
    age_data = []
    labels = []
    
    for min_age, max_age, label in age_groups:
        if max_age == 120:  # For 81+ group
            queryset = CovidData.objects.filter(age__gte=min_age)
        else:
            queryset = CovidData.objects.filter(age__gte=min_age, age__lte=max_age)
        
        # Apply country filter if specified
        if country:
            queryset = queryset.filter(country=country)
        
        aggregated = queryset.aggregate(
            total_cases=Sum('cases'),
            total_deaths=Sum('deaths'),
            total_vaccinations=Sum('vaccinations')
        )
        
        if metric == 'cases':
            value = aggregated['total_cases'] or 0
        elif metric == 'deaths':
            value = aggregated['total_deaths'] or 0
        elif metric == 'vaccinations':
            value = aggregated['total_vaccinations'] or 0
        
        age_data.append(value)
        labels.append(label)
    
    # Create Plotly bar chart
    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=age_data,
        marker_color='#2ecc71'
    )])
    
    title_prefix = f'{country} Age Group Distribution' if country else 'Age Group Distribution'
    fig.update_layout(
        title=f'{title_prefix} - {metric.title()}',
        xaxis_title='Age Groups',
        yaxis_title=f'Total {metric.title()}',
        template='plotly_white',
        height=400,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return JsonResponse({
        'graph': fig.to_json(),
        'data': list(zip(labels, age_data))
    })


def get_world_map_data(request):
    """API endpoint for world map data"""
    metric = request.GET.get('metric', 'cases')
    country = request.GET.get('country', '')
    
    # Get data by country with coordinates, optionally filtered
    queryset = CovidData.objects.all()
    if country:
        queryset = queryset.filter(country=country)
    
    country_data = queryset.values('country', 'latitude', 'longitude').annotate(
        total_cases=Sum('cases'),
        total_deaths=Sum('deaths'),
        total_vaccinations=Sum('vaccinations')
    )
    
    countries = []
    lats = []
    lons = []
    values = []
    hover_texts = []
    
    for item in country_data:
        countries.append(item['country'])
        lats.append(item['latitude'])
        lons.append(item['longitude'])
        
        if metric == 'cases':
            value = item['total_cases']
        elif metric == 'deaths':
            value = item['total_deaths']
        elif metric == 'vaccinations':
            value = item['total_vaccinations']
        
        values.append(value)
        hover_texts.append(f"{item['country']}<br>{metric.title()}: {value:,}")
    
    # Create Plotly scatter geo (no token required)
    max_value = max(values) if values else 1
    
    fig = go.Figure(data=go.Scattergeo(
        lat=lats,
        lon=lons,
        mode='markers',
        marker=dict(
            size=[max(10, min(50, val/max_value*50)) for val in values] if values else [10],
            color=values,
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title=f'{metric.title()}')
        ),
        text=hover_texts,
        hovertemplate='%{text}<extra></extra>'
    ))
    
    title_prefix = f'{country} Map' if country else 'World Map'
    fig.update_layout(
        title=f'{title_prefix} - COVID-19 {metric.title()}',
        geo=dict(
            projection_type='orthographic',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
        ),
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return JsonResponse({
        'graph': fig.to_json(),
        'data': list(zip(countries, lats, lons, values))
    })


def get_country_comparison(request):
    """API endpoint for country comparison data"""
    countries = request.GET.getlist('countries[]')
    metric = request.GET.get('metric', 'cases')
    
    if not countries:
        return JsonResponse({'error': 'No countries selected'}, status=400)
    
    comparison_data = []
    
    for country in countries:
        # Get time series data for each country
        queryset = CovidData.objects.filter(country=country).values('date').annotate(
            total_cases=Sum('cases'),
            total_deaths=Sum('deaths'),
            total_vaccinations=Sum('vaccinations')
        ).order_by('date')
        
        dates = []
        values = []
        
        for item in queryset:
            dates.append(item['date'].strftime('%Y-%m-%d'))
            if metric == 'cases':
                values.append(item['total_cases'])
            elif metric == 'deaths':
                values.append(item['total_deaths'])
            elif metric == 'vaccinations':
                values.append(item['total_vaccinations'])
        
        comparison_data.append({
            'country': country,
            'dates': dates,
            'values': values
        })
    
    # Create Plotly figure with multiple traces
    fig = go.Figure()
    
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
    
    for i, data in enumerate(comparison_data):
        color = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=data['dates'],
            y=data['values'],
            mode='lines+markers',
            name=data['country'],
            line=dict(width=3, color=color),
            marker=dict(size=6, color=color)
        ))
    
    fig.update_layout(
        title=f'Country Comparison - {metric.title()}',
        xaxis_title='Date',
        yaxis_title=f'Total {metric.title()}',
        template='plotly_white',
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return JsonResponse({
        'graph': fig.to_json(),
        'data': comparison_data
    })


def get_countries_list(request):
    """API endpoint to get list of available countries"""
    countries = CovidData.objects.values_list('country', flat=True).distinct().order_by('country')
    return JsonResponse({'countries': list(countries)})
