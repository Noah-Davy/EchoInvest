from django.contrib import admin
from .models import Portfolio

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'risk_score', 'risk_tolerance', 'created_at')
    search_fields = ('user__username', 'risk_tolerance')