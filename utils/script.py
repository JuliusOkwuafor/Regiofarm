from django.contrib.auth.models import User
from faker import Faker
from uuid import uuid4
import random
from seller.models import Seller, SellerCategory
from user.models import User, UserAddress
from post.models import Post, PostImage
from product.models import Product, ProductCategory, ProductImage


# Create a Faker instance
fake = Faker()


# Define a function to generate random user data
def generate_user():
    return User.objects.create_user(
        email=fake.email(),
        password="password123",
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        is_verified=True,
    )


# Create a seller with user relationship
user = generate_user()
seller = Seller.objects.create(
    user=user,
    category=SellerCategory.objects.get_or_create(name="Farmer")[0],
    name=fake.company(),
    ceo=fake.name(),
    vat=fake.phone_number(),
    description=fake.text(200),
    is_active=True,
    is_subscribed=True,
)

# Create some products for the seller
for i in range(3):
    product = Product.objects.create(
        seller=seller,
        category=ProductCategory.objects.get_or_create(name=fake.word())[0],
        name=fake.name(),
        description=fake.text(200),
        price=fake.pydecimal(min_value=10.0, max_value=100.0, positive=True),
        currency=random.choice(["USD", "EUR"]),
        quantity=fake.pydecimal(min_value=1.0, max_value=100.0, positive=True),
        quantity_unit=random.choice(["kg", "l", "pcs"]),
        total_quantity=fake.pydecimal(min_value=1.0, max_value=100.0, positive=True),
        is_active=True,
    )

# Create some posts for the user
for i in range(2):
    post = Post.objects.create(
        author=seller,
        headline=fake.sentence(nb_words=5),
        content=fake.text(1000),
        link=fake.url(),
        is_active=True,
        notify_followers=False,
    )

# Add some images to the post and product (assuming image paths are stored)
for model in [Post, Product]:
    for obj in model.objects.all():
        for i in range(2):
            image_path = f"{model.__name__.lower()}_{obj.id}_{i+1}.jpg"
            # Assuming you have image paths stored somewhere, use them here
            # For example, if you download images from Faker, you can use those paths
            if model == Post:
                PostImage.objects.create(post=obj, image=image_path, order=i)
            else:
                ProductImage.objects.create(product=obj, image=image_path, order=i)
