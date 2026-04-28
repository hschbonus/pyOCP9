from django import forms


class TicketForm(forms.Form):
    title = forms.CharField(max_length=128, label='Titre du ticket')
    description = forms.CharField(widget=forms.Textarea,
                                  max_length=2048,
                                  label='Description du ticket',)
    image = forms.ImageField(label='Image du ticket', required=False)


class ReviewForm(forms.Form):
    headline = forms.CharField(max_length=128, label='Titre du commentaire')
    rating = forms.IntegerField(min_value=0, max_value=5, label='Note (0-5)')
    comment = forms.CharField(widget=forms.Textarea, label='Commentaire')


class UserFollowForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur à suivre')
