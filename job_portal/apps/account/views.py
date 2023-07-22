from django.shortcuts import render,redirect
from django.views.generic import CreateView
from .forms import UserRegistrationForm,UserLoginForm
from django.urls import reverse_lazy
from django.contrib import messages
from apps.commons.utils import validate_email, authenticate_user
from django.contrib.auth import login,logout
from apps.commons.decorators import redirect_to_home_if_authenticated
from django.utils.decorators import method_decorator
from .utils import send_account_activation_mail
from .models import UserAccountActivationKey
from django.contrib.auth import get_user_model

User=get_user_model()

@method_decorator(redirect_to_home_if_authenticated,name='get')
class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'account/registration.html'
    success_url = reverse_lazy('home')
     
   
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign up'
        return context
        
    
    def post(self, request, *args,**kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            messages.success(request,"An Activation Email Has Been Sent to You")
            response= self.form_valid(form)
            user=self.object
            send_account_activation_mail(request,user)
            return response
        else:
            return self.form_invalid(form)


class UserLoginView(CreateView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('home')
    form = UserLoginForm
    
    @redirect_to_home_if_authenticated
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={"title": "login", "form": self.form()})
        
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        username_or_email = request.POST['username_or_email']   #required fields
        password=request.POST['password']

        if validate_email(username_or_email):
            user = authenticate_user(password, email=username_or_email)
            
        else:
            user = authenticate_user(password, username=username_or_email)
            
        
        if user is not None:
            login(request, user)
            messages.success(request, "User logged In Successfully !!!")
            return redirect('home')

        messages.error(request, "Invalid username or password!!")
        return redirect('user_login')


def user_logout(request):
    logout(request)
    messages.success(request,"User Logged Out!!")
    return redirect("home")

def user_account_activation(request,username,key):
    if UserAccountActivationKey.objects.filter(user__username=username,key=key):
        User.objects.filter(username=username).update(account_activated=True)
        UserAccountActivationKey.objects.filter(user__username=username).delete()
        messages.success(request,"Your Account has been Activated!!")
    else:
        messages.error(request,'Invalid Link OR The Link Has Been Expired!!')
    return redirect('user_login')


        