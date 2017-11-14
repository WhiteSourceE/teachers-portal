from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
import json
import urllib
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import CoursePageForm
from .forms import UserForm, ProfileForm

def loginForm(request):
    if request.method == 'POST':

        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST['g-recaptcha-response']
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''

        if result['success']:
	        username = request.POST['username']
	        password = request.POST['password']
	        user = authenticate(username=username, password=password)
	        if user is not None:
	            if user.is_active:
	                login(request, user)
	                return redirect('/portal/')
	            else:
	                return HttpResponse("Account Disabled.")
	        else:
	        	return render(request, 'registration/login.html', {'error_message': 'Invalid Credentials.'})
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid Captcha.'})
    if request.user.is_authenticated:
        return redirect('/portal/')
    else:
        return render(request, 'registration/login.html')

def adminForm(request):
    return render(request, 'portal/user.html')

def update_profile(request):
    if request.method == 'POST':
        if request.user.profile:
            profile_form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        else:
            profile_form = ProfileForm(request.POST,request.FILES)

        if profile_form.is_valid():
            profile_data = profile_form.save(commit=False)
            if not request.user.profile:
                profile_data.user = request.user
            profile_data.save()
            #messages.success(request, _('Your profile was successfully updated!'))
            return redirect('/portal/profile')
        #else:
            #messages.error(request, _('Please correct the error below.'))
    else:
        if request.user.profile:
            profile_form = ProfileForm(instance=request.user.profile)
        else:
            profile_form = ProfileForm()
    return render(request, 'portal/user.html', {
        'profile_form': profile_form
    })

def dashboard(request):
    # # if not request.user.is_authenticated:
    # #     return redirect('/portal/login')
    # if request.method=='POST':
    #     form = CoursePageForm(request.POST,instance=user_data)

    #     if form.is_valid():
    #         user_data = form.save()
    #         user_data.save()
    #         return redirect('/portal/profile/'+str(user))
    # else:
    #     form = CoursePageForm()
    #     return render(request, 'portal/dash.html', {'form':form})
    # return render(request,'portal/dash.html',{'form':form,})
    return render(request,'portal/dash.html')

def list_all_courses(request):
    return render(request,'portal/courses.html')