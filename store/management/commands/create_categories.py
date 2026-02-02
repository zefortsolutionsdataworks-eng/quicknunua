from django.core.management.base import BaseCommand
from store.models import Category

class Command(BaseCommand):
    help = 'Creates initial product categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Furniture',
                'description': 'Sofas, beds, tables, chairs, storage, and office furniture',
                'slug': 'furniture',
            },
            {
                'name': 'Kitchen & Utensils',
                'description': 'Cookware, kitchen appliances, utensils, and dining essentials',
                'slug': 'kitchen-utensils',
            },
            {
                'name': 'Beddings',
                'description': 'Bed sheets, blankets, pillows, duvets, and bedroom textiles',
                'slug': 'beddings',
            },
            {
                'name': 'Beauty & Personal Care',
                'description': 'Cosmetics, skincare, haircare, and personal hygiene products',
                'slug': 'beauty-personal-care',
            },
            {
                'name': 'Clothes & Fashion',
                'description': 'Men, women, and kids clothing, shoes, and accessories',
                'slug': 'clothes-fashion',
            },
            {
                'name': 'Electronics',
                'description': 'Phones, laptops, TVs, audio devices, and electronic accessories',
                'slug': 'electronics',
            },
            {
                'name': 'Home Essentials',
                'description': 'Cleaning supplies, storage solutions, and household necessities',
                'slug': 'home-essentials',
            },
        ]

        created_count = 0
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Created: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  Already exists: {category.name}'))

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Total categories created: {created_count}'))