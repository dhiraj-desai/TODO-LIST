# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404

# from .models import TodoItem
from .forms import TodoForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            # login(request, user)  # Automatically log the user in after registration
            messages.success(request, "Your account has been created successfully!")
            return redirect("todo_list")  # Redirect to any page after registration
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def todo_list(request):
    # Get to-do items for the current user only
    todos = Todo.objects.filter(user=request.user)
    print(todos)
    return render(request, "todo/todo_list.html", {"todos": todos})


@login_required
def add_todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            # Save the new to-do item, and associate it with the current user
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect("todo_list")
    else:
        form = TodoForm()
    return render(request, "todo/add_todo.html", {"form": form})


@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect("todo_list")


@login_required
def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect("todo_list")
    else:
        form = TodoForm(instance=todo)
    return render(request, "todo/update_todo.html", {"form": form})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view."})





@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
    else:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


