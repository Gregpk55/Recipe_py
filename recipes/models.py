from django.db import models
from django.core.validators import MinValueValidator

class Recipe(models.Model):
    """
    Represents a culinary recipe containing details about the dish.

    Attributes:
    - name (CharField): The name of the recipe.
    - cooking_time (FloatField): Time (in minutes) needed to prepare the dish.
    - ingredients (CharField): A comma-separated string of ingredients used.
    - description (TextField): A detailed description of the recipe.
    - pic (ImageField): An optional image representing the dish.
    """

    name = models.CharField(max_length=120, unique=True)
    cooking_time = models.FloatField(validators=[MinValueValidator(0.1)])
    ingredients = models.CharField(max_length=350)
    description = models.TextField()
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg', blank=True, null=True)

    def return_ingredients_as_list(self) -> list:
        """
        Converts the comma-separated string of ingredients into a list.

        Returns:
        - list: A list containing individual ingredients.
        """
        return [ingredient.strip() for ingredient in self.ingredients.split(",")]

    def difficulty(self) -> str:
        """
        Determines the difficulty level of the recipe based on cooking time and ingredient count.

        Difficulty Levels:
        - Easy: Cooking time < 10 mins and less than 4 ingredients.
        - Medium: Cooking time < 10 mins and 4 or more ingredients.
        - Intermediate: Cooking time >= 10 mins and less than 4 ingredients.
        - Hard: Cooking time >= 10 mins and 4 or more ingredients.

        Returns:
        - str: A string representing the difficulty level.
        """
        ingredient_count = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and ingredient_count < 4:
            return "Easy"
        elif self.cooking_time < 10 and ingredient_count >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and ingredient_count < 4:
            return "Intermediate"
        else:
            return "Hard"

    def __str__(self) -> str:
        """
        String representation of the Recipe model.

        Returns:
        - str: The name of the recipe.
        """
        return str(self.name)
