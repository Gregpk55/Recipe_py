from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import create_recipe 
from .views import home, RecipeListView, RecipeDetailView, search_recipes, signup_view, about_view

# This URL configuration is specifically for the 'recipes' app.
# It maps views to specific URL routes so that when a user navigates to a URL, 
# the corresponding view is executed.

app_name = 'recipes'

urlpatterns = [
    # Each path() call maps a URL route to a specific view.
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),  
    path('about/', about_view, name='about'),
    path('recipes/list/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('search/', search_recipes, name='search_recipes'),
    path('recipes/create/', create_recipe, name='create-recipe'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)