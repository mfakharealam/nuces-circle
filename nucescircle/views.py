from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.urls import reverse_lazy
from users.models import User, Profile, UserConnections, Recruiter
from .models import Post, Job, JobApplications
from users.models import Education
from .forms import PostForm, JobForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # like @login_required for classes
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class PostListView(UserPassesTestMixin, AjaxableResponseMixin, LoginRequiredMixin, ListView):  # home list view

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


class CreatePostView(LoginRequiredMixin, AjaxableResponseMixin, UserPassesTestMixin, CreateView):
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


class UpdatePostView(LoginRequiredMixin, AjaxableResponseMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.post_user = self.request.user
        return super().form_valid(form)

    def test_func(self):  # preventing other users from updating posts
        post = self.get_object()
        # rec = Recruiter.objects.filter(user=self.request.user)
        if self.request.user == post.post_user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, AjaxableResponseMixin, UserPassesTestMixin, DeleteView):
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
        context['previous_posted_jobs'] = Job.objects.filter(posted_by=self.request.user)  # by this user
        rec_job_app = JobApplications.objects.filter(job_applied_for__posted_by=self.request.user)
        context['rec_job_app'] = rec_job_app
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


class JobDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Job
    template_name = 'nucescircle/job_detail.html'

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        this_job_app_count = JobApplications.objects.filter(job_applied_for__pk=self.object.id).count()
        this_job_app = JobApplications.objects.filter(job_applied_for__pk=self.object.id).\
            values_list('applicant', flat=True)
        context['this_job_app_count'] = this_job_app_count
        context['this_job_apps'] = this_job_app
        context['all_users'] = User.objects.all()
        return context

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
    app, created = JobApplications.objects.get_or_create(applicant=applicant,
                                                         job_applied_for=job)
                                                         # job_poster=job.posted_by)
    return redirect('circle-jobs')


def get_posts(request):
    if request.method == 'GET' and request.is_ajax():
        # Return objects
        posts = Post.objects.all()
        ser_posts = serializers.serialize('json', posts)
        data = {
            'all_posts': ser_posts
        }
        return JsonResponse(data)


@login_required
def advanced_search(request):
    filter_by = request.GET["selection_criteria"]
    search_in = request.GET["q"]
    if filter_by == "name":
        user_objects = User.objects.filter(first_name__contains=search_in).prefetch_related('education_set')
        if not user_objects:
            user_objects = User.objects.filter(last_name__contains=search_in).prefetch_related('education_set')
    elif filter_by == "discipline":
        user_objects = User.objects.filter(education__study_field__contains=search_in).prefetch_related('education_set')
        if not user_objects:
            user_objects = User.objects.filter(education__degree__contains=search_in).prefetch_related('education_set')
    elif filter_by == "gradDate":
        user_objects = User.objects.filter(education__grad_year__contains=search_in).prefetch_related('education_set')

    return render(request, 'nucescircle/findPeople2.html', {'result': user_objects})
