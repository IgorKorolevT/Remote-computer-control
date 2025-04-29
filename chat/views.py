from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def chat(request: HttpRequest) -> HttpResponse:
    context = {
        "computers": []
    }
    return render(request, "chat/chat.html", context)