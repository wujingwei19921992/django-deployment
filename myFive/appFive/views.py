from django.shortcuts import render
from appFive.forms import UserForm,UserProfileInfoForm
# Create your views here.

# import for login logout
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request,'appFive/index.html')

#note login_required is imported from decorator above

@login_required
def special(request):
    return HttpResponse("You are loggedin, nice")

#to makesure the only user has account can user_logout
# this can be done by decorator
#makesure its 1 line above the function
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered= False
    # if there is a request:
    if request.method == "POST":
        # this imports the form from the forms.py
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Save User Form to Database
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)
            # Update with Hashed password
            user.save()

            #commit=False means we dont save data directly to databse
            #
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user =user
            # senetence abve define the 1to1 relationship
            #from modesl.py

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            # Now save model
            registered = True
        else:
            print(user_form.errors,profile_form.errors)

    # refer to te top if statement
    # else if no request:
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

        # Note
        # in registration.html we need user_form, profile_form, and registered
        # logic, so remember to pass them to html
    return render(request,'appFive/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})



def user_login(request):
    if request.method =="POST":
        username = request.POST.get('username')
        # since in the login.html, there is  input called "username"
        # you can grab that using the get method
        password = request.POST.get('password')

        user = authenticate(username=username,password =password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
                # redirect user back to home page
            else:
                return HttpResponse("Acoount not active")
        else:
            print("Username:{} and password {}".format(username,password))
            return HttpResponse("invalid login")
    else:
        return render(request,'appFive/login.html',{})
