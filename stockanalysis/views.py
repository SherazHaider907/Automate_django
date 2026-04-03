from django.shortcuts import render
from dal import autocomplete
from django.db.models import Q

from .models import Stock, StockData
from .forms import StockForm

from stocks import scrap_stock_data   

def stocks(request):
    form = StockForm()
    stock_data = None

    if request.method == "POST":
        form = StockForm(request.POST)

        if form.is_valid():
            stock = form.cleaned_data["stock"]

            data = scrap_stock_data(stock.symbol)

            stock_data = StockData.objects.create(
                stock=stock,
                current_price=data["current_price"],
                price_change=data["price_change"],
                percentage_change=data["percentage_change"],
            )

    return render(request, "stockanalysis/stocks.html", {
        "form": form,
        "stock_data": stock_data
    })


class StockAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Stock.objects.all()

        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q) |
                Q(symbol__icontains=self.q)
            )

        return qs