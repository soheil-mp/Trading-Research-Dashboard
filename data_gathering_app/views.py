
# Import the libraries
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django_pandas.io import read_frame
from .models import News
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


# Home view function 
def main(request):

    # Get all of the objects from news database
    news = News.objects.all()

    # Convert to dataframe
    df = read_frame(news)

    # Add new columns
    df["sentiment_title"] = ""
    df["sentiment_article"] = ""

    # Initialize the sentiment analysis model (i.e. FinBERT)
    tokenizer_sentiment = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model_sentiment = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

    # Classes for prediction
    classes = ['positive','negative','neutral']

    # Loop over each rows in the dataframe
    for index, row in df.iterrows():

        # Get the news title
        title = row["title"]

        # Predict the sentiment for title
        result_title = torch.softmax(model_sentiment(**tokenizer_sentiment(title, return_tensors="pt")).logits, dim=1).tolist()[0]
        result_title = [[index, i_num] for index, i_num in enumerate(result_title) if i_num==max(result_title)][0]
        result_title = "{}: {}%".format(classes[result_title[0]], int(round(result_title[1]*100)))

        # Get the article + summarize it 
        article = row["article"]
        article = article[:2000]

        # Predict the sentiment for article
        result_article = torch.softmax(model_sentiment(**tokenizer_sentiment(article, return_tensors="pt")).logits, dim=1).tolist()[0]
        result_article = [[index, i_num] for index, i_num in enumerate(result_article) if i_num==max(result_article)][0]
        result_article = "{}: {}%".format(classes[result_article[0]], int(round(result_article[1]*100)))

        # Update the values
        df.loc[index, "sentiment_title"] = result_title
        df.loc[index, "sentiment_article"] = result_article

    # Send the request + data to "home.html" template
    return render(request, "data_gathering_app/main.html", {"news_df": df})


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