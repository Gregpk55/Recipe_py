#Search, Login, Recipe Form

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RecipesSearchForm
from .models import Recipe

# Tests recipe Form
class RecipeFormTest(TestCase):
    def test_form_fields(self):
        form = RecipesSearchForm(data={'search': 'Test Recipe'})
        self.assertTrue(form.is_valid())

#Test Search View
class SearchRecipesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.url = reverse('recipes:search_recipes')
        Recipe.objects.create(
            name='Test Recipe',
            cooking_time=10,
            ingredients='Eggs, Milk',
            description='A test recipe'
        )

    def test_search_recipes_with_valid_input(self):
        response = self.client.get(self.url, {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('recipes_df', response.context)
        self.assertIn('chart', response.context)

    def test_search_recipes_context_data(self):
        response = self.client.get(self.url, {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('recipes_df' in response.context)
        self.assertTrue('chart' in response.context)

    def tearDown(self):
        self.user.delete()

#Tests Login Req Views
class LoginRequiredViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.list_url = reverse('recipes:recipe-list')
        recipe = Recipe.objects.create(name='Test Recipe', cooking_time=10, ingredients='Eggs, Milk', description='A test recipe')
        self.detail_url = reverse('recipes:recipe-detail', kwargs={'pk': recipe.pk})

    def test_list_view_with_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_with_login(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_without_login(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)  

    def test_detail_view_without_login(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 302)  

    def tearDown(self):
        self.user.delete()
        Recipe.objects.all().delete()  
