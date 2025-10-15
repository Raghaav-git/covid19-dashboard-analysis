import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from dashboard.models import CovidData


class Command(BaseCommand):
    help = 'Load COVID data from CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='COVID_CASES_Project/covid_data.csv',
            help='Path to the CSV file (default: COVID_CASES_Project/covid_data.csv)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading new data'
        )

    def handle(self, *args, **options):
        csv_file = options['file']
        
        # Check if file path is absolute, if not make it relative to project root
        if not os.path.isabs(csv_file):
            csv_file = os.path.join(settings.BASE_DIR, csv_file)
        
        if not os.path.exists(csv_file):
            raise CommandError(f'CSV file "{csv_file}" does not exist.')
        
        # Clear existing data if requested
        if options['clear']:
            self.stdout.write('Clearing existing COVID data...')
            CovidData.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))
        
        # Load data from CSV
        self.stdout.write(f'Loading data from {csv_file}...')
        
        created_count = 0
        updated_count = 0
        error_count = 0
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 since row 1 is header
                try:
                    # Parse the date
                    date = datetime.strptime(row['Date'], '%Y-%m-%d').date()
                    
                    # Create or update the record
                    covid_data, created = CovidData.objects.get_or_create(
                        country=row['Country'].strip(),
                        date=date,
                        sex=row['Sex'].strip(),
                        age=int(row['Age']),
                        defaults={
                            'cases': int(row['Cases']),
                            'deaths': int(row['Deaths']),
                            'vaccinations': int(row['Vaccinations']),
                            'confirmed_deaths_per100k': float(row['Confirmed_Deaths_per100k']),
                            'excess_deaths_per100k': float(row['Excess_Deaths_per100k']),
                            'latitude': float(row['Lat']),
                            'longitude': float(row['Lon']),
                        }
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        # Update existing record
                        covid_data.cases = int(row['Cases'])
                        covid_data.deaths = int(row['Deaths'])
                        covid_data.vaccinations = int(row['Vaccinations'])
                        covid_data.confirmed_deaths_per100k = float(row['Confirmed_Deaths_per100k'])
                        covid_data.excess_deaths_per100k = float(row['Excess_Deaths_per100k'])
                        covid_data.latitude = float(row['Lat'])
                        covid_data.longitude = float(row['Lon'])
                        covid_data.save()
                        updated_count += 1
                    
                    # Progress indicator
                    if row_num % 100 == 0:
                        self.stdout.write(f'Processed {row_num} rows...')
                        
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'Error processing row {row_num}: {e}')
                    )
                    continue
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'Data loading completed:\n'
                f'  - Created: {created_count} records\n'
                f'  - Updated: {updated_count} records\n'
                f'  - Errors: {error_count} records\n'
                f'  - Total processed: {created_count + updated_count + error_count} records'
            )
        )