
# Import the libraries
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django_pandas.io import read_frame
from .models import News
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import PegasusTokenizer, PegasusForConditionalGeneration, TFPegasusForConditionalGeneration
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
    df["sentiment_article_summary"] = ""
    df["sentiment_final"] = ""
    df["article_summary"] = ""

    # Initialize the sentiment analysis model (i.e. FinBERT)
    tokenizer_sentiment = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model_sentiment = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

    # Initialize the summarizer model
    model_name = "human-centered-summarization/financial-summarization-pegasus"
    tokenizer_summarize = PegasusTokenizer.from_pretrained(model_name)
    model_summarize = PegasusForConditionalGeneration.from_pretrained(model_name)

    # Classes for prediction
    classes = ['Good News 👍','Bad News 👎','Neutral News 🤏']

    # Loop over each rows in the dataframe
    for index, row in df.iterrows():

        # Predict the sentiment for title
        title = row["title"]
        result_title = torch.softmax(model_sentiment(**tokenizer_sentiment(title, return_tensors="pt")).logits, dim=1).tolist()[0]
        result_title_final = [[index, i_num] for index, i_num in enumerate(result_title) if i_num==max(result_title)][0]
        result_title_final = "{}: {}%".format(classes[result_title_final[0]], int(round(result_title_final[1]*100)))
        df.loc[index, "sentiment_title"] = result_title_final

        # Predict the sentiment for article
        article = row["article"]
        result_article = torch.softmax(model_sentiment(**tokenizer_sentiment(article, return_tensors="pt", max_length=512, truncation=True)).logits, dim=1).tolist()[0]
        result_article_final = [[index, i_num] for index, i_num in enumerate(result_article) if i_num==max(result_article)][0]
        result_article_final = "{}: {}%".format(classes[result_article_final[0]], int(round(result_article_final[1]*100)))
        df.loc[index, "sentiment_article"] = result_article_final

        # Summarize the article
        article = row["article"]
        article_summary = model_summarize.generate(tokenizer_summarize(article, return_tensors="pt", max_length=512, truncation=True).input_ids,  # TODO: We are truncating the article by 512 tokens (model restriction), later use a better model.
                                                    max_length=100, 
                                                    num_beams=5, 
                                                    early_stopping=True)
        article_summary = tokenizer_summarize.decode(article_summary[0], skip_special_tokens=True)  
        df.loc[index, "article_summary"] = article_summary

        # Predict the sentiment for article summary
        result_article_summary = torch.softmax(model_sentiment(**tokenizer_sentiment(article_summary, return_tensors="pt")).logits, dim=1).tolist()[0]
        result_article_summary_final = [[index, i_num] for index, i_num in enumerate(result_article_summary) if i_num==max(result_article_summary)][0]
        result_article_summary_final = "{}: {}%".format(classes[result_article_summary_final[0]], int(round(result_article_summary_final[1]*100)))
        df.loc[index, "sentiment_article_summary"] = result_article_summary_final

        # Get the final sentiment
        final_result = [(result_article[i]+result_title[i]+result_article_summary[i])/3 for i in range(3)]
        final_result = [[index, i_num] for index, i_num in enumerate(final_result) if i_num==max(final_result)][0]
        final_result = "{}: {}%".format(classes[final_result[0]], int(round(final_result[1]*100)))
        df.loc[index, "sentiment_final"] = final_result



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