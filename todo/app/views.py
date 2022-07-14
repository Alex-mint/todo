from asyncio import tasks
import json
from django.forms.models import model_to_dict
from django.shortcuts import redirect, render
from django.views.generic import View
from django.http import JsonResponse
from django.middleware.csrf import get_token
from .models import Todo
from .forms import TaskForm



class Home(View):
    def get(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            tasks = list(Todo.objects.values())
            return JsonResponse(tasks, safe=False, status=200)
        return render(request, 'todo/index.html')

    def post(self, request):
        task = json.loads(request.body)
        bound_form = TaskForm(task)

        if bound_form.is_valid():
            new_task = bound_form.save()
            return JsonResponse({'task': model_to_dict(new_task)}, status=200)
        return redirect('task')

    def delete(self, request):
        response = json.loads(request.body)
        task = Todo.objects.get(id=response.get('id'))
        task.delete()
        return JsonResponse({'result': 'ok'})

    def put(self, request):
        response = json.loads(request.body)
        task = Todo.objects.get(id=response.get('id'))
        if task.completed:
            task.completed = False
        else:
            task.completed = True
        task.save()
        return JsonResponse({'result': 'ok'})



def generate_csrf(request):
    return JsonResponse({'csrf_token': get_token(request), 'status': 200})