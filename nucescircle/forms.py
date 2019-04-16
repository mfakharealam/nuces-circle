from django import forms
from .models import Post, Job


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 15})
        }


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['job_title', 'job_desc', 'job_location', 'job_field', 'job_tags']
        labels = {
            'job_title': 'Title', 'job_location': 'Location',
            'job_field': 'Field', 'job_tags': 'Tags', 'job_desc': 'Job description'
        }
        widgets = {
            'job_desc': forms.Textarea(attrs={'rows': 5, 'cols': 1}),
        }
        # widgets = {
        #     'job_tags': forms.TextInput(attrs={'data-role': 'tagsinput', 'placeholder': 'tag1, tag2, tag3'}),
        #     'job_field': forms.Select(attrs={'class': 'bg-secondary text-white btn btn-sm'}),
        # }
