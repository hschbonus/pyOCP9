from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from blog import forms
from blog.models import Ticket


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
        ticket = Ticket.objects.get(id=ticket_id)
        if ticket.user != request.user:
            raise Http404("Vous n'avez pas la permission de modifier ce ticket.")
        form = self.form_class(instance=ticket)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
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
        ticket = Ticket.objects.get(id=ticket_id)
        if ticket.user != request.user:
            raise Http404("Vous n'avez pas la permission de supprimer ce ticket.")
        ticket.delete()
        return redirect('feed')


class ReviewTicketView(LoginRequiredMixin, View):
    template_name = 'blog/review_ticket.html'
    form_class = forms.ReviewForm

    def get(self, request, ticket_id):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form, 'ticket_id': ticket_id})

    def post(self, request, ticket_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket_id = ticket_id
            review.save()
            return redirect('feed')
        return render(request,
                      self.template_name,
                      context={'form': form, 'message': 'Erreur lors de la création de la critique.'})
