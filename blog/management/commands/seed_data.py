from django.core.management.base import BaseCommand

from authentication.models import User
from blog.models import Review, Ticket, UserFollows


class Command(BaseCommand):
    help = "Peuple la base de données avec des données de test."

    def handle(self, *args, **options):
        self._reset()
        users = self._create_users()
        tickets = self._create_tickets(users)
        self._create_reviews(users, tickets)
        self._create_follows(users)
        self.stdout.write(self.style.SUCCESS("Base de données peuplée avec succès."))

    def _reset(self):
        UserFollows.objects.all().delete()
        Review.objects.all().delete()
        Ticket.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

    def _create_users(self):
        alice = User.objects.create_user(username="alice", password="testpass123")
        bob = User.objects.create_user(username="bob", password="testpass123")
        carol = User.objects.create_user(username="carol", password="testpass123")
        self.stdout.write("  Utilisateurs créés : alice, bob, carol")
        return {"alice": alice, "bob": bob, "carol": carol}

    def _create_tickets(self, users):
        t1 = Ticket.objects.create(
            title="Critique de 1984 — George Orwell",
            description="J'aimerais avoir des avis sur ce classique de la dystopie.",
            user=users["alice"],
        )
        t2 = Ticket.objects.create(
            title="Le Meilleur des mondes — Aldous Huxley",
            description="Souvent comparé à 1984, qu'en pensez-vous ?",
            user=users["bob"],
        )
        t3 = Ticket.objects.create(
            title="Sapiens — Yuval Noah Harari",
            description="Vaut-il vraiment le détour ? Le livre est partout.",
            user=users["carol"],
        )
        t4 = Ticket.objects.create(
            title="Dune — Frank Herbert",
            description="Je cherche des critiques avant de me lancer dans cette saga.",
            user=users["alice"],
        )
        self.stdout.write("  Tickets créés : 4")
        return {"t1": t1, "t2": t2, "t3": t3, "t4": t4}

    def _create_reviews(self, users, tickets):
        # Bob répond au ticket d'Alice sur 1984
        Review.objects.create(
            ticket=tickets["t1"],
            rating=5,
            headline="Un chef-d'œuvre intemporel",
            body="1984 reste une lecture indispensable. L'écriture d'Orwell est précise et glaçante.",
            user=users["bob"],
        )
        # Carol répond au ticket d'Alice sur 1984
        Review.objects.create(
            ticket=tickets["t1"],
            rating=4,
            headline="Très bon mais dense",
            body="Excellent roman, certains passages sont lourds mais l'ensemble tient très bien.",
            user=users["carol"],
        )
        # Alice répond au ticket de Bob sur Huxley
        Review.objects.create(
            ticket=tickets["t2"],
            rating=5,
            headline="Encore plus actuel que 1984",
            body="Huxley décrit une société où le bonheur est imposé — terrifiant de pertinence.",
            user=users["alice"],
        )
        # Alice crée une critique sans ticket préalable (ticket + review simultané)
        t5 = Ticket.objects.create(
            title="Les Misérables — Victor Hugo",
            description="",
            user=users["alice"],
        )
        Review.objects.create(
            ticket=t5,
            rating=5,
            headline="Une fresque humaine monumentale",
            body="Hugo à son sommet. Incontournable.",
            user=users["alice"],
        )
        self.stdout.write("  Reviews créées : 4")

    def _create_follows(self, users):
        # alice suit bob et carol
        UserFollows.objects.create(user=users["alice"], followed_user=users["bob"])
        UserFollows.objects.create(user=users["alice"], followed_user=users["carol"])
        # bob suit alice
        UserFollows.objects.create(user=users["bob"], followed_user=users["alice"])
        # carol suit bob
        UserFollows.objects.create(user=users["carol"], followed_user=users["bob"])
        self.stdout.write("  Abonnements créés : 4")
