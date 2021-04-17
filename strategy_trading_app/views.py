
# Import the libraries
from django.shortcuts import render

# Create your views here
def main(request):
    return render(request, "strategy_trading_app/main.html", {})