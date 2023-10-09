# Recipe, Home, Details

from django.urls import reverse
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from .models import Recipe
from django.contrib.auth.models import User


# Tests for Recipe Model
class RecipeModelTest(TestCase):

    def setUp(self):
        Recipe.objects.create(
            name='Ice Water',
            cooking_time=1,
            ingredients='Ice, Water',
            description='Refreshing Ice Water'
        )

    def test_return_ingredients_as_list(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.return_ingredients_as_list(), ['Ice', 'Water'])

    def test_difficulty(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.difficulty(), 'Easy')

    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(recipe), recipe.name)

    def test_invalid_cooking_time(self):
        with self.assertRaises(ValidationError):
            invalid_recipe = Recipe(
                name='Test Recipe', 
                cooking_time=-5, 
                ingredients='Ingredient1, Ingredient2', 
                description='A test recipe'
            )
            invalid_recipe.full_clean()  #checks validation

    def test_recipe_with_no_ingredients(self):
        with self.assertRaises(ValidationError):
            invalid_recipe = Recipe(name="Test", cooking_time=5, ingredients='', description='Test description')
            invalid_recipe.full_clean()

    def test_recipe_with_zero_cooking_time(self):
        with self.assertRaises(ValidationError):
            invalid_recipe = Recipe(name="Test", cooking_time=0, ingredients='Test', description='Test description')
            invalid_recipe.full_clean()

# Tests for Home View
class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')  

    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/home.html')

    def tearDown(self):
        self.user.delete()  

# Tests for List View
class ListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')  
        
        Recipe.objects.create(
            name='Ice Water',
            cooking_time=1,
            ingredients='Ice, Water',
            description='Refreshing Ice Water'
        )

    def test_list_view_uses_correct_template(self):
        response = self.client.get(reverse('recipes:recipe-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')

    def test_list_view_displays_items(self):
        response = self.client.get(reverse('recipes:recipe-list'))
        self.assertContains(response, 'Ice Water')

    def tearDown(self):
        self.user.delete()  

#Tests for Details View
class DetailsViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')  
        
        self.recipe = Recipe.objects.create(
            name='Ice Water',
            cooking_time=1,
            ingredients='Ice, Water',
            description='Refreshing Ice Water'
        )

    def test_details_view_uses_correct_template(self):
        response = self.client.get(reverse('recipes:recipe-detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')

    def test_details_view_displays_correct_data(self):
        response = self.client.get(reverse('recipes:recipe-detail', args=[self.recipe.id]))
        self.assertContains(response, 'Ice Water')
        self.assertContains(response, 'Refreshing Ice Water')

    def test_details_view_for_non_existent_recipe(self):
        non_existent_id = self.recipe.id + 1
        response = self.client.get(reverse('recipes:recipe-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        self.user.delete()  
        self.recipe.delete()
