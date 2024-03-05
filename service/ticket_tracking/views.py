from datetime import datetime

from _decimal import Decimal

from django.shortcuts import render

from ticket_tracking.models import Event


def test(request):

    return render(request, 'home.html')
