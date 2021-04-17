
# Import the libraries
from django.contrib import admin
from .models import News

# Register the models here
@admin.register(News)
class MyAdmin(admin.ModelAdmin):
    
    # Initialize the list_display attribute for displaying the fields we want on admin list interface
    list_display = ["title", "article", "date_and_time", "source", "url"]