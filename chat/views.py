from django.http import JsonResponse
from .utils import get_csv_response
from django.shortcuts import render

def home(request):
    return render(request, 'chat/index.html')

def chat_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        response = get_csv_response(user_message)
        return JsonResponse({'response': response})

    return JsonResponse({'error': 'Invalid request'}, status=400)