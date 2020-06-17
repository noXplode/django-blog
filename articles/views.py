from django.shortcuts import render

# Create your views here.
def index(request):

    context = {
        
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'base.html', context=context)