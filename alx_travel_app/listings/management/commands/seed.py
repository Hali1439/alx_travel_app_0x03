from django.core.management.base import BaseCommand
from listings.models import Listing
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        sample_titles = ['Cozy Cottage', 'Urban Apartment', 'Beachfront Villa']
        sample_locations = ['Addis Ababa', 'Gondar', 'Hawassa']

        for i in range(10):
            Listing.objects.create(
                title=random.choice(sample_titles),
                description='A great place to stay.',
                location=random.choice(sample_locations),
                price_per_night=random.uniform(50, 300),
                available=bool(random.getrandbits(1))
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))