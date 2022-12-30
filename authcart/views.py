from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import View
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError


# Create your views here.
def signup(request):
    if (request.method=="POST"):         
        email = request.POST["email"]
        pass1 = request.POST["pass1"]     
        pass2 = request.POST["pass2"]
        if pass1 != pass2  :
            messages.warning(request, "Password is Not Matching")   
            #print("ayush")
            return render(request,'auth/signup.html')     
        try:
            if User.objects.get(username=email) and User.objects.get(username=email).is_active:
                messages.info(request, "User Already Exist")
                return render(request,'auth/login.html') 

        except Exception as identifier:
            pass

        try:
            user = None
            user = User.objects.get(username=email)
        except Exception as identifier:
            pass
        if user == None:
            user = User.objects.create_user(email,email,pass1) #email-username,email-email,pass1-password
        user.is_active=False
        user.save()
        email_subject="Activate your Account"
        message = render_to_string('auth/activate.html',{
            'user':user,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user),
        })

        email_message = EmailMessage(email_subject, message,settings.EMAIL_HOST_USER,[email])
        email_message.send()  
        messages.success(request,"Activate Your Account by clicking on the link in your gmail")
        return render(request,"auth/login.html")
    return render(request,"auth/signup.html")


class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.info(request,"Account Activated Sucessfully")
            return redirect('/authcart/login')
        return render(request,'auth/activatefail.html')
def handleLogin(request):
    if request.method == "POST":
        username = request.POST['email']
        userpassword = request.POST['pass1']
        myuser = authenticate(username=username,password=userpassword)
        if myuser is not None:
            login(request,myuser)
            # messages.success(request,'Login Success')
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials")
            render(request,"auth/login.html")
    return render(request,"auth/login.html")


    
def handleLogout(request): 
    logout(request)
    messages.info(request,"Logout Success")
    return redirect("/authcart/login")
