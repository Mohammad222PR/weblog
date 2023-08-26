from django import forms

from blogs.models import Contact, Comment


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

