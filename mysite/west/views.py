# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

def first_page(request):
    return HttpResponse("<p>西餐</p>")
# Create your views here.
