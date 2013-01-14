from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from Blogger.models import Post, Tag, Author
from django.db.models import Sum
from django.contrib import messages
from django.contrib.comments import Comment
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from Blogger.serializers import PostSerializer, AuthorSerializer
from django.utils.translation import ugettext_lazy as _
import datetime


def get_sidebar_data():

    popular_posts = Post.popular_posts.all()[:5]
    recent_posts = Post.objects.filter(
        published=True).order_by('-created_at')[:5]
    archive = Post.objects.all().dates('created_at', 'month', order='DESC')
    tags = Tag.objects.all()
    authors = Author.objects.all()
    data = {
        'popular_posts': popular_posts,
        'recent_posts': recent_posts,
        'archive': archive,
        'tags': tags,
        'authors': authors,
    }
    return data


def render_on_list(request, data):
    return render_to_response('list.html', data,
                              context_instance=RequestContext(request)
                              )


def comment_posted(request):

    c = request.GET['c']
    messages.add_message(request, messages.SUCCESS,
                         _('Commented added successfully.'))
    c = Comment.objects.get(pk=c)
    return redirect(c.content_object)


def list(request, year=None, month=None, tag=None, author=None):

    sidebar_data = get_sidebar_data()

    data = {
        'posts': None,
        'section_title': _('Posts')
    }

    data.update(sidebar_data)

    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        data['posts'] = posts
        data['section_title'] = _("Posts")
        return render_on_list(request, data)
    if author:
        fname, lname = author.split('-')
        posts = Post.objects.filter(author__first_name=fname,
                                    author__last_name=lname
                                    )
        data['posts'] = posts
        data['section_title'] = _("Posts")
        return render_on_list(request, data)
    if not year:
        posts = Post.objects.all().order_by('-created_at')
        data['posts'] = posts
        data['section_title'] = _("Posts")
        return render_on_list(request, data)
        #Recent posts reverse chrono
    if not month:
        posts = Post.objects.filter(created_at__year=year
                                    ).order_by('-created_at')
        data['posts'] = posts
        data['section_title'] = _("Yearly Archive")
        return render_on_list(request, data)
    else:
        posts = Post.objects.filter(created_at__year=year,
                                    created_at__month=month
                                    ).order_by('-created_at')
        data['posts'] = posts
        data['section_title'] = _("Monthly Archive")
        return render_on_list(request, data)


def view_post(request, slug):

    post = Post.objects.get(slug=slug)
    sidebar_data = get_sidebar_data()
    data = {
        'post': post,
    }
    data.update(sidebar_data)
    return render_to_response('view_post.html', data,
                              context_instance=RequestContext(request)
                              )


def archive_time(request):
    pass


def archive_category(request, category=None):
    pass


def archive_author(request, author=None):
    pass


# Begin API Views
@api_view
def api_root(request, format=None):
    return Response({
        'authors': reverse('authors-list', request=request),
        'posts': reverse('posts-list', request=request),
    })


class AuthorList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of users.
    """
    model = Author
    serializer_class = AuthorSerializer


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single user.
    """
    model = Author
    serializer_class = AuthorSerializer


class PostList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of groups.
    """
    model = Post
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single group.
    """
    model = Post
    serializer_class = PostSerializer
