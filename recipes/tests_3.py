#Create Recipe, User Creation

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class CreateRecipeViewTest(TestCase):

    def test_view_url_accessible_by_name(self):
        url = reverse('recipes:create-recipe')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipes/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('recipes:create-recipe')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/create_recipe.html')


class RecipeCreationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@gmail.com', password='tester')
        self.client.login(username='test', password='tester')

    def test_create_recipe(self):
        url = reverse('recipes:create-recipe')
        data = {
            'name': 'Test Pizza',
            'cooking_time': 15,
            'ingredients': 'Tomatoes, Cheese, Dough',
            'description': 'Make the dough, add ingredients, and bake.',
        }
        response = self.client.post(url, data, format='multipart')
        self.assertRedirects(response, expected_url=reverse('recipes:recipe-list'))

class UserCreationTest(TestCase):

    def test_create_user(self):
        url = reverse('recipes:signup')
        data = {'username': 'newuser', 'password1': 'testPassw0rd', 'password2': 'testPassw0rd'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  

