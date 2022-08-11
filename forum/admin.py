from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from forum.models import CategoryModel, TopicModel, PostModel


class TopicAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = TopicModel
        fields = ('description',)

class TopicAdmin(admin.ModelAdmin):
    form = TopicAdminForm
    list_display = ('id', 'username', 'title', 'created_date',)
    fieldsets = (
        (None, {'fields': ('activated', ('category', ), 'username',('title', 'created_date',), )}),
        (None, {'fields': ('description',)}),
        )


class PostAdminForm(forms.ModelForm):
    post = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = PostModel
        fields = ('post',)

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('id', 'username',)
    fieldsets = (
        (None, {'fields': ( 'activated', ('topic', 'created_date'), 'username',)}),
        (None, {'fields': ('post',)}),
        )



admin.site.register(CategoryModel)
admin.site.register(TopicModel, TopicAdmin)
admin.site.register(PostModel, PostAdmin)