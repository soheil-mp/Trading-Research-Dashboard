"""
This file provides the data layer, which Django uses to construct our database schema and queries.  
"""

# Import the libraries
from django.db import models

# Create a news model that inherites from models.Model
class News(models.Model):

    # Define the fields
    title = models.TextField()
    article = models.TextField()
    date_and_time = models.DateTimeField()
    source = models.CharField(max_length=200)
    url = models.URLField()