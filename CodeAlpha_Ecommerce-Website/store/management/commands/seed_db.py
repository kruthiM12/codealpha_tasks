from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product, UserProfile, Order, OrderItem

class Command(BaseCommand):
    help = "Seeds database with initial IndianKart categories, products, superuser and demo user."

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # 1. Superuser
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@indiankart.com', 'admin123')
            admin_user.first_name = "Admin"
            admin_user.last_name = "User"
            admin_user.save()
            UserProfile.objects.create(
                user=admin_user,
                phone='9876543210',
                address='1204 MG Road',
                city='Bengaluru',
                state='Karnataka',
                pincode='560001'
            )
            self.stdout.write("Created Superuser: admin / admin123")

        # 2. Demo User
        if not User.objects.filter(username='rahul').exists():
            user = User.objects.create_user('rahul', 'rahul.sharma@example.com', 'Password123')
            user.first_name = "Rahul"
            user.last_name = "Sharma"
            user.save()
            UserProfile.objects.create(
                user=user,
                phone='9876543210',
                address='Flat 204, Shree Residency, Baner',
                landmark='Near Axis Bank',
                city='Pune',
                state='Maharashtra',
                pincode='411045'
            )
            self.stdout.write("Created Demo User: rahul / Password123")

        # 3. Categories
        categories_data = [
            {'name': 'Fashion', 'slug': 'fashion', 'icon': '👕', 'description': 'Ethic wear, kurtas, kurtis & casual clothing'},
            {'name': 'Grocery', 'slug': 'grocery', 'icon': '🌾', 'description': 'Basmati rice, spices, organic powders & daily staples'},
            {'name': 'Electronics', 'slug': 'electronics', 'icon': '🎧', 'description': 'Earphones, gadgets & smart accessories'},
            {'name': 'Home & Kitchen', 'slug': 'home-kitchen', 'icon': '🍳', 'description': 'Cookware, bedsheets & kitchen essentials'},
            {'name': 'Beauty', 'slug': 'beauty', 'icon': '🧴', 'description': 'Ayurvedic wellness & personal care products'},
            {'name': 'Sports', 'slug': 'sports', 'icon': '🏏', 'description': 'Cricket gear, fitness equipment & outdoor items'},
            {'name': 'Books', 'slug': 'books', 'icon': '📚', 'description': 'Indian literature, history & educational books'},
        ]

        cat_objs = {}
        for c in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=c['slug'],
                defaults={'name': c['name'], 'icon': c['icon'], 'description': c['description']}
            )
            cat_objs[c['slug']] = cat

        # 4. Products
        products_data = [
            {
                'name': "Men's Cotton Ethnic Kurta",
                'category': cat_objs['fashion'],
                'price': 799.00,
                'original_price': 1199.00,
                'image': 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=600&q=80',
                'description': 'Pure breathable 100% cotton casual kurta with mandarin collar. Perfect for festive occasions, weddings, or traditional wear.',
                'stock': 35,
                'rating': 4.6,
                'num_ratings': 184,
                'is_featured': True,
                'is_popular': True
            },
            {
                'name': "Women's Printed Cotton Kurti",
                'category': cat_objs['fashion'],
                'price': 599.00,
                'original_price': 999.00,
                'image': 'https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=600&q=80',
                'description': 'Stylish A-line printed cotton kurti with three-quarter sleeves and soft breathable fabric. Daily casual & office wear.',
                'stock': 28,
                'rating': 4.7,
                'num_ratings': 210,
                'is_featured': True,
                'is_popular': True
            },
            {
                'name': "Men's Casual Linen Shirt",
                'category': cat_objs['fashion'],
                'price': 899.00,
                'original_price': 1499.00,
                'image': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=600&q=80',
                'description': 'Comfortable half-sleeve slim-fit linen shirt in pastel shade. Easy wash and light summer feel.',
                'stock': 20,
                'rating': 4.4,
                'num_ratings': 95,
                'is_featured': False,
                'is_popular': True
            },
            {
                'name': "Royal Aromatic Basmati Rice 5kg",
                'category': cat_objs['grocery'],
                'price': 499.00,
                'original_price': 650.00,
                'image': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=600&q=80',
                'description': 'Extra long grain aged Basmati rice with authentic rich aroma. Ideal for biryani, pulao and everyday meals.',
                'stock': 50,
                'rating': 4.8,
                'num_ratings': 340,
                'is_featured': True,
                'is_popular': True
            },
            {
                'name': "Organic Turmeric Powder 500g",
                'category': cat_objs['grocery'],
                'price': 199.00,
                'original_price': 250.00,
                'image': 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=600&q=80',
                'description': '100% natural, farm-fresh organic Haldi powder with high curcumin content. No artificial color or preservatives.',
                'stock': 45,
                'rating': 4.6,
                'num_ratings': 156,
                'is_featured': False,
                'is_popular': True
            },
            {
                'name': "Indian Masala Gift Pack (6 Spices)",
                'category': cat_objs['grocery'],
                'price': 449.00,
                'original_price': 599.00,
                'image': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=600&q=80',
                'description': 'Handcrafted gift set containing Garam Masala, Sambhar Powder, Chhole Masala, Biryani Spice, Kitchen King & Chaat Masala.',
                'stock': 30,
                'rating': 4.9,
                'num_ratings': 89,
                'is_featured': True,
                'is_popular': False
            },
            {
                'name': "Stainless Steel Water Bottle 1L",
                'category': cat_objs['home-kitchen'],
                'price': 349.00,
                'original_price': 499.00,
                'image': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=600&q=80',
                'description': 'Leakproof, durable food-grade 100% stainless steel flask bottle. Ergonomic grip and eco-friendly design.',
                'stock': 40,
                'rating': 4.3,
                'num_ratings': 120,
                'is_featured': False,
                'is_popular': True
            },
            {
                'name': "Hawkins Pressure Cooker 3 Litre",
                'category': cat_objs['home-kitchen'],
                'price': 1299.00,
                'original_price': 1899.00,
                'image': 'https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80',
                'description': 'Classic aluminium inner-lid pressure cooker for quick and safe cooking of dal, rice, and curries.',
                'stock': 18,
                'rating': 4.8,
                'num_ratings': 412,
                'is_featured': True,
                'is_popular': True
            },
            {
                'name': "Pure Cotton Double Bedsheet with 2 Pillow Covers",
                'category': cat_objs['home-kitchen'],
                'price': 699.00,
                'original_price': 1099.00,
                'image': 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=600&q=80',
                'description': '100% Cotton 210 TC queen/double bed sheet with vibrant Jaipuri traditional mandala prints.',
                'stock': 22,
                'rating': 4.5,
                'num_ratings': 167,
                'is_featured': False,
                'is_popular': True
            },
            {
                'name': "Wireless Neckband Bluetooth Earphones",
                'category': cat_objs['electronics'],
                'price': 899.00,
                'original_price': 1999.00,
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80',
                'description': 'Heavy bass wireless neckband with magnetic earbuds, 20 hours battery backup, and IPX5 sweat resistance.',
                'stock': 35,
                'rating': 4.4,
                'num_ratings': 290,
                'is_featured': True,
                'is_popular': True
            },
            {
                'name': "Ayurvedic Bhringraj Hair Oil 200ml",
                'category': cat_objs['beauty'],
                'price': 299.00,
                'original_price': 399.00,
                'image': 'https://images.unsplash.com/photo-1608248597261-0d29624e5be4?auto=format&fit=crop&w=600&q=80',
                'description': 'Traditional herbal hair oil enriched with Amla, Sesame, and Bhringraj extracts for hair growth and scalp nourishment.',
                'stock': 40,
                'rating': 4.6,
                'num_ratings': 142,
                'is_featured': False,
                'is_popular': False
            },
            {
                'name': "English Willow Kashmir Cricket Bat",
                'category': cat_objs['sports'],
                'price': 1499.00,
                'original_price': 2299.00,
                'image': 'https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=600&q=80',
                'description': 'Full size short handle cricket bat made from selected grain Kashmir willow with rubber grip.',
                'stock': 12,
                'rating': 4.7,
                'num_ratings': 98,
                'is_featured': True,
                'is_popular': False
            },
            {
                'name': "The Discovery of India by Jawaharlal Nehru",
                'category': cat_objs['books'],
                'price': 399.00,
                'original_price': 500.00,
                'image': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=600&q=80',
                'description': 'Masterpiece written during imprisonment in 1942–1946, detailing Indian philosophy, history and culture.',
                'stock': 25,
                'rating': 4.9,
                'num_ratings': 310,
                'is_featured': False,
                'is_popular': True
            }
        ]

        for p in products_data:
            Product.objects.get_or_create(
                name=p['name'],
                defaults=p
            )

        self.stdout.write("Database seeding completed successfully!")
