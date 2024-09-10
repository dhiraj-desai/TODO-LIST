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


# @api_view(["POST"])
# def register(request):
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(
#             {"message": "User created successfully."}, status=status.HTTP_201_CREATED
#         )
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# def todo_list(request):
#     todos = TodoItem.objects.all()  # Retrieve all to-do items

#     if request.method == 'POST':
#         if 'todo_id' in request.POST:  # Check if we're updating an existing item
#             todo_id = request.POST.get('todo_id')
#             todo = get_object_or_404(TodoItem, id=todo_id)
#             form = TodoForm(request.POST, instance=todo)
#         else:  # Adding a new item
#             form = TodoForm(request.POST)

#         if form.is_valid():
#             form.save()  # Save the data (either new or updated)
#             return redirect('todo_list')  # Redirect to the same page to display updated data

#     else:
#         form = TodoForm()  # Provide an empty form for adding new items

#     return render(request, 'todo/todo_list.html', {'todos': todos, 'form': form})

# def delete_todo(request, todo_id):
#     todo = get_object_or_404(TodoItem, id=todo_id)
#     todo.delete()
#     return redirect(todo_list)


# def item_list(request):
#     if request.method == 'POST':
#         form = ItemForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             return redirect(item_list)  # Redirect to the same view to display the updated list
#     else:
#         form = ItemForm()

#     items = Item.objects.all()  # Fetch all items from the database
#     return render(request, 'todo/items_list.html', {'form': form, 'items': items})

#     # if 'my_list' not in request.session:
#     #     request.session['my_list'] = []


#     # if request.method == 'POST':

#     #     new_item = request.POST.get('item')
#     #     if new_item:
#     #         request.session['my_list'].append(new_item)
#     #         request.session.modified = True

#     #     return redirect(form_list_view)

#     # # Pass the updated list to the template for display
#     # return render(request, 'todo/index.html', {'my_list': request.session['my_list']})

# def tlist(request):
#     pass
#     # return render(request, "todo/index.html")


# def update_item_view(request):

#     if request.method == 'POST':

#         item_index = int(request.POST.get('item_index'))
#         updated_item = request.POST.get('updated_item')
#         form = ItemForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             return redirect(item_list)  # Redirect to the same view to display the updated list
#         else:
#             form = ItemForm()

#         items = Item.objects.all()  # Fetch all items from the database
#         return render(request, 'todo/items_list.html', {'form': form, 'items': items})

#     #     if 'my_list' in request.session and updated_item:
#     #         my_list = request.session['my_list']
#     #         if 0 <= item_index < len(my_list):
#     #             my_list[item_index] = updated_item  # Update the item in the list
#     #             request.session.modified = True
#     #     return redirect(form_list_view)


# def delete_item_view(request):
#     pass
#     # if request.method == 'POST':
#     #     item_index = int(request.POST.get('item_index'))
#     #     # Remove the item from the list using its index
#     #     if 'my_list' in request.session:
#     #         my_list = request.session['my_list']
#     #         if 0 <= item_index < len(my_list):
#     #             del my_list[item_index]
#     #             request.session.modified = True
#     #     return redirect(form_list_view)
