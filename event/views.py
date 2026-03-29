from django.contrib.auth.decorators import login_required, async_to_sync
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from chat.utils import send_message_to_computer


@login_required
def block(request: HttpRequest, name: str) -> HttpResponse:
    user = request.user
    computers = user.computers.all()
    chosen_computer = get_object_or_404(computers, name=name)
    async_to_sync(send_message_to_computer)(user, chosen_computer, "taskkill /IM notepad.exe /F")
    return render(request, "event/block.html")

