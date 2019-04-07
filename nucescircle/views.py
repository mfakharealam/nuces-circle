from django.shortcuts import render, redirect
from users.models import User
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # like @login_required but for classes instead
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

# Create your views here.

# handle user requests and routes


@login_required
def home(request):
    create_form = PostForm(request.POST, instance=request.user)
    # update_form = PostForm(request.POST, instance=request.user)
    # update_form.fields = request.user.post.content
    context = {
        'posts': Post.objects.all(),
        'create_form': create_form,
    }
    return render(request, 'nucescircle/home.html', context)


class PostListView(LoginRequiredMixin, ListView):  # home list view
    model = Post
    template_name = 'nucescircle/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'  # as in def home
    ordering = ['-post_date']  # latest post order

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['create_form'] = PostForm()
        return context


class PostDetailView(LoginRequiredMixin, DetailView):  # home list view
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    context_object_name = 'form'

    def form_valid(self, form):
        form.instance.post_user = self.request.user
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.post_user = self.request.user
        return super().form_valid(form)

    def test_func(self):  # preventing other users from updating posts
        post = self.get_object()
        if self.request.user == post.post_user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # home list view
    model = Post
    success_url = '/'

    def test_func(self):  # preventing other users from updating posts
        post = self.get_object()
        if self.request.user == post.post_user:
            return True
        return False


@login_required
def about(request):
    return render(request, 'nucescircle/about.html')


@login_required
def my_circle(request):
    return render(request, 'nucescircle/MyCircle.html')


@login_required
def recruit(request):
    return render(request, 'nucescircle/Recruit.html')


@login_required
def find_people(request):
    return render(request, 'nucescircle/findPeople2.html')


def login(request):
    return render(request, 'nucescircle/newLogin.html')


@login_required
def jobs_listing(request):
    return render(request, 'nucescircle/JobsListing.html')


@login_required
def profile_editing(request):
    return render(request, 'nucescircle/profileEditing.html')


def search(request):
    filter_by = request.GET["q"]
    user_objects = User.objects.filter(username__contains=filter_by).prefetch_related('education_set')
    return render(request, 'nucescircle/results.html', {'result': user_objects})
