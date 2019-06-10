from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def register_user(request):
    print(" I am Here @@@@@@@@@@@@@@@@@@@@@")
    return render(request, '' , {})