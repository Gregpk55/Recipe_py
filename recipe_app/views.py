from django.shortcuts import render, redirect  
#Django authentication libraries           
from django.contrib.auth import authenticate, login, logout
#Django Form for authentication
from django.contrib.auth.forms import AuthenticationForm   
 

def login_view(request):   
   """
    Renders the login page and handles the user authentication process.
    
    Args:
        request: HttpRequest object.
    
    Returns:
        HttpResponseRedirect to 'recipes:home' if authentication is successful.
        Otherwise, renders the login page with any error messages.
    """                         
   error_message = None                            
   form = AuthenticationForm()                            


   if request.method == 'POST':                         
       form =AuthenticationForm(data=request.POST)

       #check if form is valid
       if form.is_valid():                                
           username=form.cleaned_data.get('username')     
           password = form.cleaned_data.get('password')    

           #use Django authenticate function to validate the user
           user=authenticate(username=username, password=password)
           if user is not None:           

               login(request, user)                
               return redirect('recipes:home') 
           error_message ='ooops.. something went wrong'   

   #prepare data to send from view to template
   context ={                                             
       'form': form,                                
       'error_message': error_message                     
   }
   #load the login page using "context" information
   return render(request, 'auth/login.html', context)   


def logout_view(request):
    """
    Log out the current user and redirect to home.
    
    Args:
        request: HttpRequest object.
    
    Returns:
        HttpResponseRedirect to 'recipes:home'.
    """
    logout(request)
    return redirect('recipes:home')  


