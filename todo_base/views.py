from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task


class CustomLoginView(LoginView):
    template_name = 'todo_base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task-list')


class RegisterView(FormView):
    template_name = 'todo_base/register.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse_lazy('task-list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task-list')
        return super().get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)

        query = self.request.GET.get('query', "")
        if query:
            context['tasks'] = context['tasks'].filter(title__icontains=self.request.GET['query'])
        context['query'] = query
        context['count'] = context['tasks'].filter(complete=False).count()
        return context


# class TaskSearch(LoginRequiredMixin, ListView):
#     model = Task
#     context_object_name = 'tasks'
#
#     def get_context_data(self, **kwargs):
#         context = super(TaskList, self).get_context_data(**kwargs)
#         context['tasks'] = context['tasks'].filter(user=self.request.user)
#         context['count'] = context['tasks'].filter(complete=False).count()
#         return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task-list')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')




