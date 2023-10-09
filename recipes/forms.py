from django import forms
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

CHART_TYPE_CHOICES = [
    ('', 'Select Chart Type'),
    ('#1', 'Bar Chart'),
    ('#2', 'Pie Chart'),
    ('#3', 'Line Chart'),
]

GRAPH_DATA_TYPE_CHOICES = [
    ('cooking_time', 'Cooking Time'),
    ('difficulty', 'Difficulty'),
]


class RecipesSearchForm(forms.Form):
    """
    Form for searching recipes by name or ingredients and 
    selecting the type of chart and data for visualization.
    """
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search recipes or ingredients', 'class': 'search_input'}),
        help_text='Enter a recipe name or ingredient.'
    )
    chart_type = forms.ChoiceField(
        required=False,
        choices=CHART_TYPE_CHOICES,
        initial='#1',
        widget=forms.Select(attrs={'class': 'chart_type_select'}),
        help_text='Select the type of chart to display.'
    )
    graph_data_type = forms.ChoiceField(
        required=False,
        choices=GRAPH_DATA_TYPE_CHOICES,
        initial='cooking_time',
        widget=forms.Select(attrs={'class': 'graph_data_type_select'}),
        help_text='Select the type of data to plot.'
    )

class RecipeCreateForm(forms.ModelForm):
    """
    Form for creating a new recipe or editing an existing one.
    """
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'cooking_time', 'description', 'pic']
        

class SignUpForm(UserCreationForm):
    """
    Custom sign-up form for user registration.
    Extends Django's default UserCreationForm.
    """
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )