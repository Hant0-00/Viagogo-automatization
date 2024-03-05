from django.db import models

class Event(models.Model):
    event = models.CharField(max_length=200)
    data_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    number_event = models.BigIntegerField()
    source_link = models.URLField(null=True, blank=True)
    manager = models.CharField(max_length=200, null=True, blank=True)
    announcement_number = models.BigIntegerField()
    sector = models.CharField(max_length=200)
    ticket_quantity = models.IntegerField()
    link_viagogo = models.URLField(null=True, blank=True)
    features = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=100)
    source_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    net_price = models.DecimalField(max_digits=6, decimal_places=2)
    min_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    commission = models.FloatField(default=1.015)
    coefficient = models.FloatField(null=True, blank=True)
    profit_percentage = models.IntegerField(null=True, blank=True)
    bot = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.source_price:
            self.min_price = float(self.source_price) * self.coefficient * 1.1111 * self.commission
            self.max_price = float(self.source_price) * 1.66 * 1.1111 * self.commission
            self.profit_percentage = (float(self.source_price) - float(self.net_price)) / self.source_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event} - {str(self.number_event)}"