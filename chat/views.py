from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import get_csv_response

@login_required
def chat_home(request):
    return render(request, 'chat/index.html')

@login_required
def chat_response(request):
    if request.method == 'POST':
        try:
            user_message = request.POST.get('message', '')
            response = get_csv_response(user_message)
        except Exception as e:
            response = str(e)
        return JsonResponse({'response': response})

    return JsonResponse({'error': 'Invalid request'}, status=400)