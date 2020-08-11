from .models import Article, Comment
from .forms import CommentForm, SearchForm

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.core.paginator import Paginator
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.db.models import Q

# main page
def index(request, tag=None):

    popular_tags = getpopulartags()
    latest_comments = Comment.objects.filter(showing = True)[:5]
    
    context = { 
            'popular_tags' : popular_tags,
            'latest_comments' : latest_comments,
        }

    if request.GET:
        form = SearchForm(request.GET)
        if form.is_valid() and 'search_string' in form.cleaned_data:
            search_string = form.cleaned_data['search_string']
            search_result = get_search_result(search_string)
        
            contextsearch = {
                'search_string' : search_string, 
                'artiсles' : search_result,
                'form' : form,
            }
            context.update(contextsearch)
            return render(request, 'articles/search.html', context=context)
        else:
            return HttpResponseRedirect(reverse('articles:index') )

    else:
        form = SearchForm()

        artiсles = Article.objects.filter(status = 'p')
        
        if tag:
            artiсles = artiсles.filter(tags__name__in=[tag])

        paginator = Paginator(artiсles, 6) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        contextblog = { 
            'artiсles' : page_obj,
            'tag' : tag,
            'form' : form,
        }
        context.update(contextblog)

        return render(request, 'articles/blog.html', context=context)

def getpopulartags():
    artiсles = Article.objects.filter(status = 'p')[:30]
    tagscount = {}
    poptags = []
    for article in artiсles:
        t = article.tags.names()
        for tag in t:
            if tag in tagscount:
                tagscount[tag] += 1
            else:
                tagscount[tag] = 1
    #print(tagscount)
    for key in tagscount:
        if tagscount[key] > 1:
            poptags.append(key)
    return poptags

def get_search_result(phrase):
    words = phrase.split(' ')
    temp = Article.objects.none() #empty set
    for word in words:
        obj_list = Article.objects.filter(Q(text__icontains=word) | Q(title__icontains=word)).distinct()
        obj_list.union(temp)
    return list(set(obj_list))

# article page
class ArticleView(FormMixin, generic.DetailView):   #https://docs.djangoproject.com/en/3.0/topics/class-based-views/mixins/#using-formmixin-with-detailview
    model = Article
    template_name = 'articles/article.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('articles:viewpost', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            if request.POST.get('parent', None):
                parent_id = request.POST.get('parent')
                return self.form_valid(form, parent_id)
            else:
                return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, parent_id=None):
        new_comment = form.save(commit=False)
        new_comment.article = self.object
        if parent_id:
            new_comment.parent = Comment.objects.get(pk=parent_id)
        new_comment.save()
        return super().form_valid(form)
