from django.shortcuts import render

# Create your views here.

import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# Create your views here.

class EarningsTemplateView(LoginRequiredMixin, TemplateView):
    """
    Lists employees for a given user
    """
    login_url = "/login/"
    template_name = 'earnings/earnings.html'
    
