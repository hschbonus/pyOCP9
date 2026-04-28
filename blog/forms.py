from django import forms

from blog.models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']


class UserFollowForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur à suivre')
