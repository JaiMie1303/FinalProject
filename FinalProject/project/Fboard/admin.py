from django.contrib import admin

from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Reply)
admin.site.register(Media)
# admin.site.register(PostAdmin)