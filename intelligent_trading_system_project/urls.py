"""intelligent_trading_system_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Import the libraries
from django.contrib import admin
from django.urls import path

# Import all the view functions
from starting_page_app import views as starting_page_views
from dashboard_app import views as dashboard_views
from data_gathering_app import views as data_gathering_views
from portfolio_selection_app import views as portfolio_selection_views
from rl_trading_app import views as rl_trading_views
from strategy_trading_app import views as strategy_trading_views


# Define the url patterns
urlpatterns = [

    path('admin/', admin.site.urls),

    path('', starting_page_views.main, name="starting_page"),

    path('dashboard/', dashboard_views.main, name="dashboard"),

    path('dashboard/data_gathering/', data_gathering_views.main, name="data_gathering"),
    path('dashboard/data_gathering/stocks/<str:stock_name>/',   data_gathering_views.stock_details, name="stock_detail"),
    path('dashboard/data_gathering/news/<int:news_index>',      data_gathering_views.news_detail,   name="news_detail"),

    path('dashboard/portfolio_selection/', portfolio_selection_views.main, name="portfolio_selection"),
    path('dashboard/rl_trading/', rl_trading_views.main, name="rl_trading"),
    path('dashboard/strategy_trading/', strategy_trading_views.main, name="strategy_trading"),
]
