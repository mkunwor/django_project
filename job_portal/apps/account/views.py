from django.shortcuts import render
from django.views.generic import CreateView
from .forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.contrib import messages


class UserRegistration(CreateView):
    form_class = UserRegistrationForm
    template_name = 'account/registration.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign up'
        return context
        
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            messages.success(request,"User Created Successfully")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)