from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length=250)
    symbol = models.CharField(max_length=50)
    sector = models.CharField(max_length=200,null=True, blank=True)
    exchange = models.CharField(max_length=100)
    country = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name
    

class StockData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="data")

    # Prices (use FloatField)
    current_price = models.FloatField(null=True, blank=True)
    price_change = models.FloatField(null=True, blank=True)
    percentage_change = models.FloatField(null=True, blank=True)

    previous_close = models.FloatField(null=True, blank=True)
    week_52_high = models.FloatField(null=True, blank=True)
    week_52_low = models.FloatField(null=True, blank=True)

    market_cap = models.BigIntegerField(null=True, blank=True)
    pe_ratio = models.FloatField(null=True, blank=True)
    dividend_yield = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.stock.symbol} - {self.current_price}"