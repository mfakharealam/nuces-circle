from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from users.models import User, Profile, UserConnections, Recruiter
from .models import Post, Job, JobApplications
from .forms import PostForm, JobForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # like @login_required for classes
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required


class PostListView(UserPassesTestMixin, LoginRequiredMixin, ListView):  # home list view

    model = Post

    template_name = 'nucescircle/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'  # as in def home
    ordering = ['-post_date']  # latest post order

    def test_func(self):
        if not self.request.user.is_anonymous:
            rec = Recruiter.objects.filter(user=self.request.user)
            if rec:
                redirect('circle-recruit')
                return False
            return True

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['create_form'] = PostForm()
        p = Profile.objects.filter(user=self.request.user).first()
        connected_users = p.friends.all().count()
        req = UserConnections.objects.filter(to_user=self.request.user).count()
        context['connected_count'] = connected_users
        context['requests_count'] = req
        return context


class PostDetailView(LoginRequiredMixin, DetailView):  # home list view
    model = Post


class CreatePostView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['content']
    context_object_name = 'form'

    def form_valid(self, form):
        form.instance.post_user = self.request.user
        return super().form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     rec = Recruiter.objects.filter(user=self.request.user)
    #     if rec:
    #         return redirect('circle-recruit')
    #     else:
    #         return super(CreatePostView, self).get(request, *args, **kwargs)

    def test_func(self):
        rec = Recruiter.objects.filter(user=self.request.user)
        if rec:
            return False
        return True


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.post_user = self.request.user
        return super().form_valid(form)

    def test_func(self):  # preventing other users from updating posts
        post = self.get_object()
        rec = Recruiter.objects.filter(user=self.request.user)
        if self.request.user == post.post_user and rec is None:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):  # preventing other users from updating posts
        post = self.get_object()
        rec = Recruiter.objects.filter(user=self.request.user)
        if self.request.user == post.post_user and rec is None:
            return True
        return False


@login_required
def about(request):
    return render(request, 'nucescircle/about.html')


@login_required
def my_circle(request):
    rec = Recruiter.objects.filter(user=request.user)
    if rec:
        return redirect('circle-recruit')
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


class JobListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Job
    template_name = 'nucescircle/Recruit.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'previous_posted_jobs'
    ordering = ['-date_posted']  # latest job order

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context['job_form'] = JobForm()
        return context

    def test_func(self):
        rec = Recruiter.objects.filter(user=self.request.user)
        if rec:
            return True
        return False


class CreateJobView(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['job_title', 'job_desc', 'job_location', 'job_field', 'job_tags']
    context_object_name = 'job_form'

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        rec = Recruiter.objects.filter(user=self.request.user)
        if rec:
            return True
        return False


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('circle-recruit')

    def test_func(self):  # preventing other users from updating posts
        rec = Recruiter.objects.filter(user=self.request.user)
        job = self.get_object()
        if self.request.user == job.posted_by and rec:
            return True
        return False


@login_required
def find_people(request):
    rec = Recruiter.objects.filter(user=request.user)
    if rec:
        return redirect('circle-recruit')
    return render(request, 'nucescircle/findPeople2.html')


def login(request):
    return render(request, 'nucescircle/newLogin.html')


@login_required
def jobs_listing(request):
    rec = Recruiter.objects.filter(user=request.user)
    jobs = Job.objects.all()
    applied_jobs = JobApplications.objects.filter(applicant=request.user).values_list('job_applied_for', flat=True)
    context = {'jobs_posted': jobs, 'applied_jobs': applied_jobs}
    if rec:
        return redirect('circle-recruit')
    return render(request, 'nucescircle/JobsListing.html', context)


@login_required
def profile_editing(request):
    return render(request, 'nucescircle/profileEditing.html')


@login_required
def search(request):
    filter_by = request.GET["q"]
    user_objects = User.objects.filter(username__contains=filter_by).prefetch_related('education_set')
    return render(request, 'nucescircle/results.html', {'result': user_objects})


@login_required
def add_job_applicant(request, *args, **kwargs):
    job_id = int(kwargs['jid'])
    applicant = request.user
    job = get_object_or_404(Job, pk=job_id)
    app, created = JobApplications.objects.get_or_create(applicant=applicant, job_applied_for=job)
    return redirect('circle-jobs')
