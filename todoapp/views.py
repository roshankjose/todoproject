from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .forms import TodoForm
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from .models import Task


class TaskListView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'task1'

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name', 'priority', 'date')
    success_url = reverse_lazy('cbvdetail')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('cbvhome')

class TaskDetailView(DetailView):  # Define the TaskDetailView
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'

def demo(request):
    if request.method == 'POST':
        name = request.POST.get('task', '')
        priority = request.POST.get('priority', '')
        date = request.POST.get('date', '')

        # Validate the priority field
        try:
            priority = int(priority)
        except ValueError:
            # If priority is not a valid integer, set it to a default value or handle the error as needed
            priority = 1  # Set a default value, for example

        # Validate the date field
        if not date:
            raise ValidationError('Date field is required.')

        task = Task(name=name, priority=priority, date=date)
        task.save()

    task1 = Task.objects.all()
    return render(request, 'home.html', {'task1': task1})

def delete(request, taskid):
    task = Task.objects.get(id=taskid)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, 'delete.html')

def update(request, id):  # Define the update view function
    task = Task.objects.get(id=id)
    f = TodoForm(request.POST or None, instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')  # Redirect to the home page
    return render(request, 'edit.html', {'f': f, 'task': task})
