from django.template import Library
from articles.models import Article, Comment

register = Library()

@register.simple_tag
def populartags():
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

@register.simple_tag
def latestcomments(qt=5):
     return Comment.objects.filter(showing = True)[:qt]