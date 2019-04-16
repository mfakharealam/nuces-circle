from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from users.models import User, Profile, UserConnections
from .models import Post, Job
from .forms import PostForm, JobForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # like @login_required for classes
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

# Create your views here.

# handle user requests and routes


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


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
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
    p = Profile.objects.get(user=request.user)
    friends = p.friends.all()
    sent_friend_requests = UserConnections.objects.filter(from_user=request.user)
    rec_friend_requests = UserConnections.objects.filter(to_user=request.user)  # if anyone have sent requests to me
    context = {
        'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests
    }
    return render(request, 'nucescircle/MyCircle.html', context)


class JobListView(LoginRequiredMixin, ListView):  # home list view
    model = Job
    template_name = 'nucescircle/Recruit.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'previous_posted_jobs'  # as in def home
    ordering = ['-date_posted']  # latest job order

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context['job_form'] = JobForm()
        return context


class CreateJobView(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['job_title', 'job_desc', 'job_location', 'job_field', 'job_tags']
    context_object_name = 'job_form'

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('circle-recruit')

    def test_func(self):  # preventing other users from updating posts
        job = self.get_object()
        if self.request.user == job.posted_by:
            return True
        return False


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
