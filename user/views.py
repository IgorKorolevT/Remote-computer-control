from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Create your views here.
# def login_view(request):
#     username = request.POST["username"]
#     password = request.POST["password"]
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#     else:
#         ...


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "base.html")
