from .models import Article
from .forms import CommentForm

from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator
from django.views.generic.edit import FormMixin
from django.urls import reverse

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
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return super().form_valid(form)