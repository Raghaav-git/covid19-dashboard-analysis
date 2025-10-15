from django.db import models

class CovidData(models.Model):
    """Model to store COVID-19 data by country, date, gender, and age"""
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    country = models.CharField(max_length=100, db_index=True)
    date = models.DateField(db_index=True)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    cases = models.PositiveIntegerField()
    deaths = models.PositiveIntegerField()
    vaccinations = models.PositiveIntegerField()
    confirmed_deaths_per100k = models.FloatField()
    excess_deaths_per100k = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "COVID Data"
        verbose_name_plural = "COVID Data"
        ordering = ['-date', 'country', 'sex', 'age']
        unique_together = [['country', 'date', 'sex', 'age']]
        indexes = [
            models.Index(fields=['country', 'date']),
            models.Index(fields=['date', 'sex']),
            models.Index(fields=['country', 'sex']),
        ]
    
    def __str__(self):
        return f"{self.country} - {self.date} - {self.get_sex_display()} - Age {self.age}"
