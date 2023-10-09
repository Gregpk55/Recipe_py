from io import BytesIO
import base64
import matplotlib.pyplot as plt
from .models import Recipe
import re  # Importing re module


def get_difficulty_data():
    """
    Fetches the count of recipes per difficulty level.
    
    Returns:
        dict: A dictionary containing the count of recipes for each difficulty.
    """
    difficulty_data = {'Easy': 0, 'Medium': 0, 'Intermediate': 0, 'Hard': 0}
    try:
        for recipe in Recipe.objects.all():
            difficulty = recipe.difficulty()
            difficulty_data[difficulty] = difficulty_data.get(difficulty, 0) + 1
    except Exception as e:
        print(f"An error occurred: {e}")
    return difficulty_data


def get_cooking_time_chart(chart_type, data):
    """
    Generates a chart based on the cooking time for each recipe.

    Args:
        chart_type (str): The type of chart to be drawn.
        data (DataFrame): DataFrame containing the cooking time data.
    """
    # Apply the HTML tag stripping to the 'name' 
    data['name'] = data['name'].apply(lambda x: re.sub('<.*?>', '', x))
    try:
        if chart_type not in ['#1', '#2', '#3']:
            raise ValueError("Invalid chart type provided")
        
        if chart_type == '#1':  # bar chart
            plt.bar(data['name'], data['cooking_time'], label='Time (minutes)')
        elif chart_type == '#3':  # line chart
            plt.plot(data['name'], data['cooking_time'], marker='o', label='Time (minutes)')
        elif chart_type == '#2':  # pie chart
            plt.pie(data['cooking_time'], labels=data['name'], autopct='%1.1f%%')
        
        if chart_type in ['#1', '#3']:
            plt.xticks(fontsize=8, rotation=45)

        if chart_type != '#2':
            plt.legend()
    except Exception as e:
        print(f"An error occurred while drawing cooking time chart: {e}")


def get_difficulty_chart(chart_type, queryset=None):
    """
    Generates a chart representing the difficulty of each recipe.

    Args:
        chart_type (str): The type of chart to be drawn.
        queryset (QuerySet, optional): QuerySet containing recipe data. Defaults to None.
    """
    try:
        if chart_type not in ['#1', '#2', '#3']:
            raise ValueError("Invalid chart type provided")
        
        if queryset is None:
            queryset = Recipe.objects.all()
        
        all_recipes = queryset
        recipe_pairs = [(recipe.difficulty(), recipe.name) for recipe in all_recipes]
        difficulties, recipe_names = zip(*recipe_pairs)
        
        if chart_type in ['#1', '#3']:  # Bar or Line chart
            difficulty_levels = {'Easy': 1, 'Medium': 2, 'Intermediate': 3, 'Hard': 4}
            y = [difficulty_levels[difficulty] for difficulty in difficulties]
            if chart_type == '#1':  # Bar chart
                plt.bar(recipe_names, y, label='Difficulty Level')
            elif chart_type == '#3':  # Line chart
                plt.plot(recipe_names, y, marker='o', label='Difficulty Level')
            plt.yticks(list(difficulty_levels.values()), list(difficulty_levels.keys()))
            
            if chart_type in ['#1', '#3']:  
                plt.xticks(fontsize=8, rotation=45)  
        elif chart_type == '#2':  # Pie chart
            difficulty_data = get_difficulty_data()
            plt.pie(list(difficulty_data.values()), labels=difficulty_data.keys(), autopct='%1.1f%%')
        
        if chart_type != '#2':
            plt.legend()
    except Exception as e:
        print(f"An error occurred while drawing difficulty chart: {e}")


def get_chart(chart_type, data=None, chart_data_type='cooking_time', queryset=None):
    """
    Generates a chart based on the provided data and chart type.
    
    This function uses Matplotlib to generate charts. The generated chart is then
    converted into a base64-encoded PNG image which can be embedded in web pages.
    
    Parameters:
        chart_type (str): The type of chart ('#1' for Bar, '#2' for Pie, '#3' for Line).
        data (DataFrame, optional): The data for the chart. Defaults to None.
        chart_data_type (str, optional): Specifies the type of data to be plotted 
                                         ('cooking_time' or 'difficulty'). Defaults to 'cooking_time'.
        queryset (QuerySet, optional): An optional Django QuerySet to retrieve data from. Defaults to None.

    Returns:
        str: A base64-encoded PNG representation of the chart.
        
    Raises:
        ValueError: If an unsupported chart data type is provided.
    """
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(13, 8))
    plt.clf()

    if chart_type not in ['#1', '#2', '#3']:
        chart_type = '#1'

    try:
        if chart_data_type == 'cooking_time':
            get_cooking_time_chart(chart_type, data)
        elif chart_data_type == 'difficulty':
            get_difficulty_chart(chart_type, queryset)
        else:
            raise ValueError(f"Unsupported chart data type: {chart_data_type}")
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png).decode('utf-8')
        return graph
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        plt.close(fig)
        if 'buffer' in locals():
            buffer.close()
