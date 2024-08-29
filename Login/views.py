from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from Bid.utils import send_mail



def call_function(request):
    return redirect("/login")

def initiate_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_obj = User.objects.get(username=email)
        user = authenticate(username=email, password=password)
        request.session['context'] = {
            "fullName": user_obj.first_name + " " + user_obj.last_name,
            "email": user_obj.username,
            "uuid": str(user_obj.customuser.unique_key)
        }
        print("user- ", user)
        if user is not None:
            return redirect("option_of_trading")
            
        else:
           return HttpResponse("Sorry... You Are Not Authenticated.")

    return render(request, 'welcome.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            if User.objects.filter(username=email).exists():
                return HttpResponse("Email already exists.")
            user = User.objects.create_user(email, password=password, first_name= username.split(" ")[0], last_name= username.split(" ")[1])
            user.save()
            subject = "User Creation Successful"
            message = f"Dear {username.split(" ")[0]}, You have successfully registered on TradeSquare. Your login_id = {email} and password = {password}"
            from_email = "rohansaha9477@gmail.com"
            if subject and message and from_email:
                send_mail(message, email)
                return redirect('initiate_login')
            else:
                return HttpResponse("Make sure all fields are entered and valid.")
        except Exception as e:
            return HttpResponse(e)
    
    return render(request, 'register.html')
