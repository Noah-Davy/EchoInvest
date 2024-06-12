# app_advisor/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField


class Portfolio(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    risk_score = models.IntegerField()
    risk_tolerance = models.CharField(max_length=255)
    portfolio_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portfolio of {self.user.username}"