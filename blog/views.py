from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from blog import forms
from blog.models import Review, Ticket


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
