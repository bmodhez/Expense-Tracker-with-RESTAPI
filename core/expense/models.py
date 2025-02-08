from typing import Iterable
from django.db import models

# Create your models here.

class Transactions(models.Model):
        title = models.CharField(max_length=100)
        amount = models.FloatField()
        type = models.CharField(max_length=100, choices=(("CREDIT", "CREDIT"), ("DEBIT", "DEBIT")))

        def __str__(self):
                return f"{self.title} --- {self.type} by {self.amount}"

        def save(self, *args, **kwargs):
                if self.type == "DEBIT":
                        self.amount = self.amount * -1 
                return super().save(*args, **kwargs)