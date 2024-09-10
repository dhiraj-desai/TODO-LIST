from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['task', 'completed']

        error_messages = {
            'task':{
                "required": "Your task must not be empty",
                "max_length": "Please enter a shorter task"
            }
        }

    



