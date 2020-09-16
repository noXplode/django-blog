from .models import Article, Comment
from .views import get_search_result

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    password = 'example'


class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    user = factory.SubFactory(UserFactory)
    title = 'Test Article title'
    slug = factory.Sequence(lambda n: f'test_slug_{n}')
    text = 'Test Acticle text'
    status = 'p'    # published


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    article = factory.SubFactory(ArticleFactory)
    name = 'Test Name'
    text = 'Test Comment text'


class ArticleModelTests(TestCase):

    def test_str_method(self):
        """
        __str__() must return title
        """
        article = ArticleFactory()
        self.assertEqual(article.__str__(), ArticleFactory.title)

    def test_get_absolute_url_method(self):
        """
        get_absolute_url() returns article url
        """
        article = ArticleFactory()
        response = reverse('articles:viewpost', args=[article.slug])
        self.assertEqual(article.get_absolute_url(), response)

    def test_get_nonparent_comments_method(self):
        """
        get_nonparent_comments() returns non replies comments
        """
        article = ArticleFactory()
        comment = CommentFactory.create(article=article)
        comment2 = CommentFactory.create(article=article, parent=comment)
        self.assertEqual(len(article.get_nonparent_comments()), 1)


class CommentModelTests(TestCase):

    def test_str_method(self):
        """
        __str__() must return comment test
        """
        comm = CommentFactory()
        self.assertEqual(comm.__str__(), CommentFactory.text)


class ViewsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 7+1 articles for pagination tests
        ArticleFactory.create_batch(7)
        another_article = ArticleFactory(text='new test')
        another_article.tags.add('test')

    def test_index_template(self):
        """
        index() uses articles/blog.html template
        index() returns status_code 200
        """
        response = self.client.get(reverse('articles:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/blog.html")

    def test_posts_pagination(self):
        """
        Posts must paginate by 6
        """
        response = self.client.get(reverse('articles:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['artiсles']) == 6)

    def test_posts_pagination_page(self):
        """
        Second page must have 1 post
        """
        response = self.client.get(reverse('articles:index') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['artiсles']) == 2)

    def test_posts_pagination_404_page(self):
        """
        Third page must not exist
        """
        response = self.client.get(reverse('articles:index') + '?page=3')
        self.assertEqual(response.status_code, 404)

    def test_index_with_search(self):
        """
        when searching index() uses articles/search.html template
        text must be found 7 times on test articles
        """
        response = self.client.get(reverse('articles:index') + '?search_string=text')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/search.html")
        self.assertTrue(len(response.context['artiсles']) == 7)

    def test_index_template_with_tag(self):
        """
        index() uses articles/blog.html template
        index() returns status_code 200
        articles count = 1 on test data
        """
        response = self.client.get(reverse('articles:tagfilter', args=['test']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/blog.html")
        self.assertTrue(len(response.context['artiсles']) == 1)

    def test_search_def(self):
        """
        Search for phrase test
        """
        self.assertEqual(len(get_search_result('text')), 7)
        self.assertEqual(len(get_search_result('new')), 1)

    def test_articleview_template(self):
        """
        ArticleView uses articles/article.html template
        ArticleView returns status_code 200
        """
        article = Article.objects.get(pk=1)
        response = self.client.get(reverse('articles:viewpost', args=[article.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/article.html")

    def test_articleview_valid_commentform(self):
        """
        form must be valid with test comment
        """
        article = Article.objects.get(pk=1)
        data = {'name': 'test name', 'text': 'test comment text'}
        response = self.client.post(reverse('articles:viewpost', args=[article.slug]), data)
        self.assertEqual(response.status_code, 302)

    def test_articleview_valid_commentform_with_parent(self):
        """
        form must be valid with child test comment
        """
        article = Article.objects.get(pk=1)
        comment = CommentFactory(article=article)
        data = {'name': 'test name', 'text': 'test comment text', 'parent': comment.pk}
        response = self.client.post(reverse('articles:viewpost', args=[article.slug]), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(article.get_nonparent_comments()), 1)
        self.assertEqual(len(article.comment_set.filter(parent__isnull=False)), 1)
