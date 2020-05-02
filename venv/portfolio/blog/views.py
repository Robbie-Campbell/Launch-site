from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import( 
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView
)
from .models import post, announcement

def home(request):

    posts = post.objects.all()
    context = {
        "posts" : posts
    }
     
    return render(request, 'blog/home.html', context)


def announcements(request):
    latest_announcement_list = announcement.objects.all()
    context = {
        "announcement": latest_announcement_list,
    }
    return render(request, 'blog/announcements.html', context)

class PostListView(ListView):
    model = post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'about'})

class SearchView(ListView):
    model = post
    template_name = 'blog/search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
          postresult = post.objects.filter(title__contains=query,
                                           content__contains=query)
          result = postresult
        else:
           result = None
        return result