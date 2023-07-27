from django.shortcuts import render
from django.views.generic import ListView
from .pagination import CustomPagination
from .models import Job,Category
from apps.commons.utils import get_base_url

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
        

        


