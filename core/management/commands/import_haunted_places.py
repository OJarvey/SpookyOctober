"""
Management command to import haunted places from CSV file.

Usage:
    python manage.py import_haunted_places path/to/haunted_places.csv
"""

import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from core.models import Location, HauntedPlace


class Command(BaseCommand):
    help = 'Import haunted places from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file containing haunted places data'
        )
        parser.add_argument(
            '--user',
            type=str,
            default='admin',
            help='Username of the user to assign as creator (default: admin)'
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing haunted places if they already exist (based on location name)'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        username = options['user']
        update_existing = options['update']

        # Get the user who will be the creator
        try:
            creator = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist. Please create the user first.')

        self.stdout.write(self.style.NOTICE(f'Starting import from {csv_file}'))
        self.stdout.write(self.style.NOTICE(f'Creator: {creator.username}'))

        # Read and process CSV
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                imported_count = 0
                updated_count = 0
                skipped_count = 0

                for row_num, row in enumerate(reader, start=2):  # Start at 2 to account for header
                    try:
                        self.stdout.write(f'\nProcessing: {row["name"]}...')

                        # Create or update Location
                        location, created = Location.objects.get_or_create(
                            name=row['name'],
                            defaults={
                                'address': row['address'],
                                'city': row['city'],
                                'state': row['state'],
                                'zip_code': row['zip_code'],
                                'country': row['country'],
                                'location_type': row['location_type'],
                                'created_by': creator,
                                'is_verified': True  # Auto-verify imported locations
                            }
                        )

                        if not created:
                            # Update existing location
                            location.address = row['address']
                            location.city = row['city']
                            location.state = row['state']
                            location.zip_code = row['zip_code']
                            location.country = row['country']
                            location.location_type = row['location_type']
                            location.save()
                            self.stdout.write(self.style.WARNING(f'  → Updated existing location: {location.name}'))

                        # Create or update HauntedPlace
                        try:
                            haunted_place = HauntedPlace.objects.get(location=location)

                            if update_existing:
                                # Update existing haunted place
                                haunted_place.story_title = row['story_title']
                                haunted_place.story_content = row['story_content']
                                haunted_place.historical_context = row['historical_context']
                                haunted_place.scare_level = int(row['scare_level'])
                                haunted_place.year_established = int(row['year_established']) if row['year_established'] else None
                                haunted_place.reported_phenomena = row['reported_phenomena']
                                haunted_place.famous_for = row['famous_for']
                                haunted_place.view_count = int(row['view_count']) if row['view_count'] else 0
                                haunted_place.visit_count = int(row['visit_count']) if row['visit_count'] else 0
                                haunted_place.save()

                                updated_count += 1
                                self.stdout.write(self.style.SUCCESS(f'  ✓ Updated: {haunted_place.story_title}'))
                            else:
                                skipped_count += 1
                                self.stdout.write(self.style.WARNING(f'  → Skipped (already exists): {haunted_place.story_title}'))

                        except HauntedPlace.DoesNotExist:
                            # Create new haunted place
                            haunted_place = HauntedPlace.objects.create(
                                location=location,
                                story_title=row['story_title'],
                                story_content=row['story_content'],
                                historical_context=row['historical_context'],
                                scare_level=int(row['scare_level']),
                                year_established=int(row['year_established']) if row['year_established'] else None,
                                reported_phenomena=row['reported_phenomena'],
                                famous_for=row['famous_for'],
                                created_by=creator,
                                view_count=int(row['view_count']) if row['view_count'] else 0,
                                visit_count=int(row['visit_count']) if row['visit_count'] else 0,
                            )

                            imported_count += 1
                            self.stdout.write(self.style.SUCCESS(f'  ✓ Imported: {haunted_place.story_title}'))

                    except KeyError as e:
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ Error on row {row_num}: Missing column {e}')
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ Error on row {row_num}: {str(e)}')
                        )

                # Summary
                self.stdout.write('\n' + '='*50)
                self.stdout.write(self.style.SUCCESS(f'Import completed!'))
                self.stdout.write(f'  • New imports: {imported_count}')
                self.stdout.write(f'  • Updated: {updated_count}')
                self.stdout.write(f'  • Skipped: {skipped_count}')
                self.stdout.write('='*50)

        except FileNotFoundError:
            raise CommandError(f'File "{csv_file}" not found.')
        except Exception as e:
            raise CommandError(f'Error reading CSV file: {str(e)}')
