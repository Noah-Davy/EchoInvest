# app_advisor/models.py
from django.db import models
from django.conf import settings


class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    risk_score = models.IntegerField()
    risk_tolerance = models.CharField(max_length=255)
    portfolio_data = models.JSONField()  # To store the portfolio allocation and performance as JSON

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portfolio of {self.user.username}"
