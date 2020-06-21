from .models import Article

from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator

# Create your views here.
def index(request, tag=None):

    artiсles = Article.objects.filter(status = 'p')

    if tag:
        artiсles = artiсles.filter(tags__name__in=[tag])

    paginator = Paginator(artiсles, 6) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = { 
        'artiсles' : page_obj,
        'tag' : tag,
    }

    return render(request, 'articles/blog.html', context=context)

class ArticleView(generic.DetailView):
    model = Article
    template_name = 'articles/article.html'