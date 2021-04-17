
# Import the libraries
from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import News


# Home view function
def main(request):

    # Send HTML codes directly
    #return HttpResponse("<h1>THIS IS THE HOME PAGE.</h1>")

    # Get all of the objects from news database
    news = News.objects.all()

    # Send the request + data to "home.html" template
    return render(request, "data_gathering_app/main.html", {"news": news})


# Stock detail view function
def stock_details(request, stock_name):

    # Send HTML codes directly
    #return HttpResponse("<h1>LET'S TAKE A LOOK AT THE {} STOCK.</h1>".format(stock_name))

    # TODO: Get that specific stock deatil online
    try:
        #stock = News.objects.get(stock_name=stock_name)
        stock = None
    
    # Show 404 error if there isn't such stock
    except:
        raise Http404("OOPS! STOCK NOT FOUND!")

    # Send the request + data to "stock_details.html" template
    return render(request, "data_gathering_app/stock_details.html", {"stock": stock})


# Stock detail view function
def news_detail(request, news_index):

    # Get all of the objects from news database
    i_news = News.objects.get(id=news_index)

    # Send the request + data to "news_detail.html" template
    return render(request, "data_gathering_app/news_detail.html", {"i_news": i_news})    