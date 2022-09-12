from django.shortcuts import render
from django.shortcuts import redirect
from .models import Person, Task
from django.http import HttpResponse

user = None
removed = False

def main(request):
    global user, removed
    if removed:
        removed = False
        return render(request, "main.html", {
                "tasks": Person.objects.get(user_name=user).task_set.all(),
                "user_name": user,
                "login": True})
    elif request.POST:
        try:
            prsn = Person.objects.get(user_name=request.POST['user_name'])
        except:
            return render(request, "login.html", {"wrong_user_name": True})
        if prsn.password == request.POST['password']:
            user = prsn.user_name
            return render(request, "main.html", {
                "tasks": prsn.task_set.all(),
                "user_name": user,
                "login": True
                })
        else:
            return render(request, "login.html", {"wrong_password": True})
    elif request.GET and user:
        task = request.GET["input_task"]
        if task:
            owner = Person.objects.get(user_name=user)
            task = Task(task_content= task, owner= owner)
            task.save()
            return render(request, "main.html", {
                    "tasks": owner.task_set.all(),
                    "user_name": user,
                    "login": True
                    })
        else:
            prsn = Person.objects.get(user_name=user)
            return render(request, "main.html", {
                "tasks": prsn.task_set.all(),
                "user_name": user,
                "login": True
                })
    return render(request, "main.html", {"login": False})

def sign(request):
    if request.POST:
        context = {
            "user_name": request.POST['user_name'],
            "password": request.POST['password'],
        }
        prsn = Person()
        prsn.user_name = context["user_name"]
        prsn.password = context["password"]
        global user
        user = prsn.user_name
        try:
            prsn.save()
        except:
            return render(request, "sign_up.html", {"already_exist": True})
        task = Task(task_content='delete me', owner=prsn)
        task.save()
        context["login"] = True
        context["tasks"] = prsn.task_set.all()
        return render(request, "main.html", context)
    return render(request, "sign_up.html")

def login(request):
    return render(request, "login.html")

def remove(request, id):
    global removed
    try:
        task = Task.objects.get(id=id)
    except:
        return HttpResponse('stop playing')
    if str(task.owner) == user:
        task.delete()
        removed = True
        return redirect('main')
    else:
        return HttpResponse('there is a pb')



