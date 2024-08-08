import json
from django.shortcuts import render
from app_users.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from curriculum.models import Standard
from .models import UserProfileInfo, Contact
from django.views.generic import CreateView
from .forms import SimpleForm
from django.shortcuts import render
# from .openai_service import generate_response
from django.shortcuts import render
from .services.openai_service import get_gpt_response
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
import requests
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# openai.api_key = settings.OPENAI_API_KEY

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")
        else:
            return HttpResponse("Please use correct id and password")
            # return HttpResponseRedirect(reverse('register'))

    else:
        return render(request, 'app_users/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# Create your views here.
# def index(request):
#     return render(request,'app_users/index.html')

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'app_users/registration.html',
                            {'registered':registered,
                             'user_form':user_form,
                             'profile_form':profile_form})

class HomeView(TemplateView):
    template_name = 'app_users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        standards = Standard.objects.all()
        teachers = UserProfileInfo.objects.filter(user_type='teacher')
        context['standards'] = standards
        context['teachers'] = teachers
        return context

class ContactView(CreateView):
    model = Contact
    fields = '__all__'
    template_name = 'app_users/contact.html'

def simple_form_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return 1
        # HttpResponseRedirect('/success/')
    else:
        form = UserForm()

    return render(request, 'app_users/simple_form.html', {'form': form})


# your_app/views.py

# from django.shortcuts import render
# from .services.openai_service import get_gpt_response

# def chat_view(request):
#     if request.method == 'POST':
#         prompt = request.POST.get('prompt', '')
#         response = get_gpt_response(prompt)
#         return render(request, 'app_users/chat.html', {'response': response})
#     return render(request, 'app_users/chat.html')


    # return render(request, 'your_app/chat.html')

# @method_decorator(csrf_exempt, name='dispatch')
# class chat_View(View):

#     def post(self, request, *args, **kwargs):
#         try:
#             # Assuming request contains the necessary data
#             data = json.loads(request.body)
#             user_message = data.get("message")

#             # OpenAI API call
#             response = openai.ChatCompletion.create(
#                 model="gpt-4",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": user_message}
#                 ]
#             )

#             # Extract response message
#             ai_message = response['choices'][0]['message']['content']

#             # Return the response as JSON
#             return JsonResponse({"message": ai_message}, status=200)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

# Hugging Face API configuration
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# @csrf_exempt
# def chat_View(request):
@csrf_exempt
def chat_View(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('input', '')
            
            # Replace this with your actual model query
            response = query({"inputs": user_input})
            bot_response = response[0]['generated_text']
            bot_response = bot_response[len(user_input):].strip()
            
            return JsonResponse({'response': bot_response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


def chat_page(request):
    return render(request, 'chat.html')


# @csrf_exempt
# def chat_View(request):
#     if request.method == 'GET':
#         return HttpResponse('This is a GET response')
#     elif request.method == 'POST':
#         return HttpResponse('This is a POST response')
#     else:
#         return HttpResponse('Method not allowed', status=405)