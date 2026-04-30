from itertools import chain

from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.db.models import Q, CharField, Value

from blog import forms
from blog.models import Review, Ticket, UserFollows


class CreateTicketView(LoginRequiredMixin, View):
    template_name = 'blog/create_ticket.html'
    form_class = forms.TicketForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
        return render(request,
                      self.template_name,
                      context={'form': form, 'message': 'Erreur lors de la création du ticket.'})


class UpdateTicketView(LoginRequiredMixin, View):
    template_name = 'blog/update_ticket.html'
    form_class = forms.TicketForm

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if ticket.user != request.user:
            raise Http404("Vous n'avez pas la permission de modifier ce ticket.")
        form = self.form_class(instance=ticket)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if ticket.user != request.user:
            raise Http404("Vous n'avez pas la permission de modifier ce ticket.")
        form = self.form_class(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('feed')
        return render(request,
                      self.template_name,
                      context={'form': form, 'message': 'Erreur lors de la mise à jour du ticket.'})


class DeleteTicketView(LoginRequiredMixin, View):
    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if ticket.user != request.user:
            raise Http404("Vous n'avez pas la permission de supprimer ce ticket.")
        ticket.delete()
        return redirect('feed')


class CreateReviewView(LoginRequiredMixin, View):
    template_name = 'blog/review_ticket.html'
    form_class = forms.ReviewForm

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = self.form_class()
        return render(request, self.template_name, context={'form': form, 'ticket': ticket})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket_id = ticket_id
            review.save()
            return redirect('feed')
        return render(request,
                      self.template_name,
                      context={'form': form,
                               'ticket': ticket,
                               'message': 'Erreur lors de la création de la critique.'})


class UpdateReviewView(LoginRequiredMixin, View):
    template_name = 'blog/update_review.html'
    form_class = forms.ReviewForm

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if review.user != request.user:
            raise Http404("Vous n'avez pas la permission de modifier cette critique.")
        form = self.form_class(instance=review)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if review.user != request.user:
            raise Http404("Vous n'avez pas la permission de modifier cette critique.")
        form = self.form_class(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('feed')
        return render(request,
                      self.template_name,
                      context={'form': form, 'message': 'Erreur lors de la mise à jour de la critique.'})


class DeleteReviewView(LoginRequiredMixin, View):
    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if review.user != request.user:
            raise Http404("Vous n'avez pas la permission de supprimer cette critique.")
        review.delete()
        return redirect('feed')


class CreateTicketAndReviewView(LoginRequiredMixin, View):
    template_name = 'blog/create_ticket_and_review.html'
    ticket_form_class = forms.TicketForm
    review_form_class = forms.ReviewForm

    def get(self, request):
        ticket_form = self.ticket_form_class()
        review_form = self.review_form_class()
        return render(request,
                      self.template_name,
                      context={'ticket_form': ticket_form, 'review_form': review_form})

    def post(self, request):
        ticket_form = self.ticket_form_class(request.POST, request.FILES)
        review_form = self.review_form_class(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect('feed')

        return render(request,
                      self.template_name,
                      context={'ticket_form': ticket_form,
                               'review_form': review_form,
                               'message': 'Erreur lors de la création du ticket et de la critique.'})


class SubscriptionsView(LoginRequiredMixin, View):
    template_name = 'blog/subscriptions.html'
    form_class = forms.UserFollowForm

    def get(self, request):
        user_follow_form = self.form_class()
        followed_users = UserFollows.objects.filter(user=request.user)
        followers = UserFollows.objects.filter(followed_user=request.user)
        return render(request, self.template_name, context={'followed_users': followed_users,
                                                            'followers': followers,
                                                            'user_follow_form': user_follow_form})

    def post(self, request):
        user_follow_form = self.form_class(request.POST)
        if user_follow_form.is_valid():
            username_to_follow = user_follow_form.cleaned_data['username']
            try:
                user_to_follow = get_user_model().objects.get(username=username_to_follow)
                if user_to_follow == request.user:
                    raise ValueError("Vous ne pouvez pas vous suivre vous-même.")
                UserFollows.objects.get_or_create(user=request.user, followed_user=user_to_follow)
            except get_user_model().DoesNotExist:
                return render(request,
                              self.template_name,
                              context={'message': f"L'utilisateur '{username_to_follow}' n'existe pas.",
                                       'user_follow_form': user_follow_form,
                                       'followed_users': UserFollows.objects.filter(user=request.user),
                                       'followers': UserFollows.objects.filter(followed_user=request.user)})
            except ValueError as e:
                return render(request,
                              self.template_name,
                              context={'message': str(e),
                                       'user_follow_form': user_follow_form,
                                       'followed_users': UserFollows.objects.filter(user=request.user),
                                       'followers': UserFollows.objects.filter(followed_user=request.user)})

            return redirect('subscriptions')

        followed_users = UserFollows.objects.filter(user=request.user)
        followers = UserFollows.objects.filter(followed_user=request.user)
        return render(request, self.template_name, context={
            'user_follow_form': user_follow_form,
            'followed_users': followed_users,
            'followers': followers,
        })


class DeleteFollowView(LoginRequiredMixin, View):
    def post(self, request, followed_user_id):
        followed_user = get_object_or_404(get_user_model(), id=followed_user_id)
        follow_instance = get_object_or_404(UserFollows, user=request.user, followed_user=followed_user)
        follow_instance.delete()
        return redirect('subscriptions')


class PostsPageView(LoginRequiredMixin, View):
    template_name = 'blog/posts.html'

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user).annotate(
            content_type=Value('TICKET', CharField())
        )
        reviews = Review.objects.filter(user=request.user).annotate(
            content_type=Value('REVIEW', CharField())
        )
        posts = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created, reverse=True)
        return render(request, self.template_name, context={'posts': posts})


class FeedPageView(LoginRequiredMixin, View):
    template_name = 'blog/feed.html'

    def get(self, request):
        followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)

        tickets = Ticket.objects.filter(
            Q(user__in=followed_users) |
            Q(user=request.user)
        )
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        reviews = Review.objects.filter(
            Q(user__in=followed_users) |
            Q(user=request.user) |
            Q(ticket__user=request.user)
        ).distinct()
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created, reverse=True)

        context = {
            'tickets_and_reviews': tickets_and_reviews,
        }
        return render(request, self.template_name, context=context)
