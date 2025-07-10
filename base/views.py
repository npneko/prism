from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
    View
)

from .models import Task


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")
    

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('task_list')


class RegisterView(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('task_list')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('task_list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'base/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        
        search_input = self.request.GET.get('search-area', '').strip()
        if search_input:
            queryset = queryset.filter(
                Q(title__icontains=search_input) | 
                Q(description__icontains=search_input)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incomplete_count'] = self.get_queryset().filter(complete=False).count()
        context['search_input'] = self.request.GET.get('search-area', '')
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'base/task_detail.html'
    context_object_name = 'task'
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'base/task_form.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'base/task_form.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task_list')
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'base/task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task_list')
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)