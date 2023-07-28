from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .pagination import CustomPagination
from .models import Job,Category,JobApplication
from apps.commons.utils import get_base_url
from django.contrib import messages
from django.shortcuts import redirect
from apps.commons.utils import is_profile_complete
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(ListView):
    template_name = 'core/home.html'
    pagination_class = CustomPagination
    queryset = Job.objects.filter(is_active=True)

    def get_queryset(self):
        category=self.request.GET.get('category')
        search=self.request.GET.get("search")
        filter_dict={"is_active":True}
        exclude=dict()
        if self.request.user.is_authenticated:
            exclude.update(job_application__user=self.request.user)
        if category:
            filter_dict.update(category__uuid=category)
        if search:
            filter_dict.update(title__icontains=search)
        return Job.objects.filter(**filter_dict).exclude(**exclude).order_by('id') # ** makes dynamic filter
    
    
    def get_pagination(self):
        return self.pagination_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        pagination = self.get_pagination()
        qs = pagination.get_paginated_qs(view=self)
        nested_qs = pagination.get_nested_pagination(qs, nested_size=2)
        context['job_lists'] = nested_qs
        context['categories']=Category.objects.all()
        context['base_ur']=get_base_url(request=self.request)
        page_number,page_str=pagination.get_current_page(view=self)
        context[page_str]='active'
        context['next_page']=page_number+1
        context['prev_page']=page_number-1
        if page_number>= pagination.get_last_page(view=self):
            context['next']='disabled'
        if page_number<=1:
            context['previous']='disabled'
        context['home_active']='active'

        return context
        
class JobDetailView(DetailView):
    template_name='core/job_detail.html'
    queryset=Job.objects.filter(is_active=True)
    slug_field='uuid' #this must be unique field from table
    slug_url_kwarg='uuid'  #this must be exactly from url
    context_object_name='job'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] ="JOb Detail" 
        return context
    

@login_required
def job_apply(request,uuid):
    try:
        job=Job.objects.get(uuid=uuid)
    except Job.DoesNotExist:
        messages.error(request,"Something went wrong!!")
        return redirect('home')
    
    if is_profile_complete(request.user): #Aplly for job
        JobApplication.objects.get_or_create(user=request.user,job=job,defaults={"status":"APPLIED"})
        messages.success(request,f"You've Successfully Applied for The Role of {job.title}")
        return redirect('home')
    messages.error(request,"Please activate your account and complete your profile")
    return redirect('home')

@method_decorator(login_required,name='dispatch')
class MyJobsView(ListView):
    template_name='core/my_job.html'
    
    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)
    
