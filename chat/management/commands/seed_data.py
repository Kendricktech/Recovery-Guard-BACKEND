import random
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from chat.models import Message
from cases.models import Case, SupportingDocuments
from faker import Faker
from django.conf import settings
from django.core.management import call_command
import os
from django.core.files import File

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seeds the database with random data for testing purposes.'

    def handle(self, *args, **options):
        # Create random users
        self.stdout.write(self.style.SUCCESS('Creating random users...'))
        agents = []
        customers = []
        for _ in range(10):
            agent = User.objects.create_user(
                email=fake.email(),
                password="password123",
                is_agent=True,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                username=fake.user_name(),
            )
            agents.append(agent)

            customer = User.objects.create_user(
                email=fake.email(),
                password="password123",
                is_customer=True,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                username=fake.user_name(),
            )
            customers.append(customer)

        self.stdout.write(self.style.SUCCESS(f'Created {len(agents)} agents and {len(customers)} customers.'))

        # Create random cases
        self.stdout.write(self.style.SUCCESS('Creating random cases...'))
        cases = []
        for _ in range(20):
            case = Case.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                agent=random.choice(agents),
                customer=random.choice(customers),
                status=random.choice(['open', 'in_progress', 'closed']),
                priority=random.choice(['low', 'normal', 'high']),
                resolution_status=random.choice(['unresolved', 'resolved', 'pending']),
            )
            cases.append(case)

        self.stdout.write(self.style.SUCCESS(f'Created {len(cases)} cases.'))

        # Create random messages
        self.stdout.write(self.style.SUCCESS('Creating random messages...'))
        for _ in range(50):
            case = random.choice(cases)
            sender = random.choice([case.agent, case.customer])
            receiver = case.customer if sender == case.agent else case.agent
            message = Message.objects.create(
                case=case,
                sender=sender,
                receiver=receiver,
                subject=fake.sentence(),
                content=fake.text(),
                timestamp=fake.date_time_this_year(),
                is_read=random.choice([True, False]),
            )

            # Optionally add random files (image, document, voice_note)
            if random.choice([True, False]):
                message.image = self.generate_fake_file('image')
            if random.choice([True, False]):
                message.document = self.generate_fake_file('document')
            if random.choice([True, False]):
                message.voice_note = self.generate_fake_file('voice_note')

            message.save()

        self.stdout.write(self.style.SUCCESS('Created random messages.'))

        # Optionally create supporting documents for cases
        self.stdout.write(self.style.SUCCESS('Creating random supporting documents for cases...'))
        for case in cases:
            for _ in range(random.randint(0, 3)):  # Random number of supporting docs
                SupportingDocuments.objects.create(
                    case=case,
                    file=self.generate_fake_file('document'),
                )

        self.stdout.write(self.style.SUCCESS('Created supporting documents.'))

        # Ensure the admin user gets testing data filled in
        self.stdout.write(self.style.SUCCESS('Ensuring admin user gets testing data...'))
        try:
            admin_user = User.objects.get(email='admin@gmail.com')
        except User.DoesNotExist:
            admin_user = User.objects.create_superuser(
                email='admin@gmail.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                username='adminuser',
            )

        # Add random cases, messages, and supporting documents for the admin account
        for _ in range(5):  # Create 5 cases for the admin user for testing purposes
            case = Case.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                agent=random.choice(agents),
                customer=admin_user,
                status=random.choice(['open', 'in_progress', 'closed']),
                priority=random.choice(['low', 'normal', 'high']),
                resolution_status=random.choice(['unresolved', 'resolved', 'pending']),
            )

            # Create random messages for this case
            for _ in range(5):  # Create 5 messages per case for the admin
                sender = random.choice([case.agent, case.customer])
                receiver = case.customer if sender == case.agent else case.agent
                message = Message.objects.create(
                    case=case,
                    sender=sender,
                    receiver=receiver,
                    subject=fake.sentence(),
                    content=fake.text(),
                    timestamp=fake.date_time_this_year(),
                    is_read=random.choice([True, False]),
                )

                # Add random files (image, document, voice_note) to the message
                if random.choice([True, False]):
                    message.image = self.generate_fake_file('image')
                if random.choice([True, False]):
                    message.document = self.generate_fake_file('document')
                if random.choice([True, False]):
                    message.voice_note = self.generate_fake_file('voice_note')

                message.save()

            # Add supporting documents for this case
            for _ in range(random.randint(0, 3)):  # Random number of supporting docs
                SupportingDocuments.objects.create(
                    case=case,
                    file=self.generate_fake_file('document'),
                )

        self.stdout.write(self.style.SUCCESS('Admin user testing data has been filled.'))

    def generate_fake_file(self, file_type):
        """Generate a fake file for testing purposes."""
        # Determine the directory where files will be stored
        media_dir = os.path.join(settings.MEDIA_ROOT, file_type)
        os.makedirs(media_dir, exist_ok=True)  # Create subdirectories for each file type (image, document, voice_note)

        if file_type == 'image':
            # Fetch a random image from Unsplash
            image_url = "https://source.unsplash.com/random/800x600"
            response = requests.get(image_url)
            if response.status_code == 200:
                file_name = f"{file_type}_{fake.uuid4()}.jpg"
                file_path = os.path.join(media_dir, file_name)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                return File(open(file_path, 'rb'), name=file_name)

        elif file_type == 'voice_note':
            # Download a random MP3 file from a public source
            mp3_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
            response = requests.get(mp3_url)
            if response.status_code == 200:
                file_name = f"{file_type}_{fake.uuid4()}.mp3"
                file_path = os.path.join(media_dir, file_name)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                return File(open(file_path, 'rb'), name=file_name)

        else:
            # For documents (PDFs)
            fake_file_name = f'{file_type}_{fake.uuid4()}.pdf'
            file_path = os.path.join(media_dir, fake_file_name)
            with open(file_path, 'wb') as f:
                f.write(b"Fake document content.")
            
            return File(open(file_path, 'rb'), name=fake_file_name)
