import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_add_detailed_product_to_cart"),
    ]

    operations = [
        migrations.CreateModel(
            name="Wishlist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="생성일시")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="수정일시")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wishlist",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="사용자",
                    ),
                ),
            ],
            options={
                "verbose_name": "위시리스트",
                "verbose_name_plural": "위시리스트 목록",
                "db_table": "wishlists",
            },
        ),
        migrations.CreateModel(
            name="WishlistItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="생성일시")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="수정일시")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wishlisted_items",
                        to="products.product",
                        verbose_name="상품",
                    ),
                ),
                (
                    "wishlist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="orders.wishlist",
                        verbose_name="위시리스트",
                    ),
                ),
            ],
            options={
                "verbose_name": "위시리스트 항목",
                "verbose_name_plural": "위시리스트 항목 목록",
                "db_table": "wishlist_items",
            },
        ),
        migrations.AddConstraint(
            model_name="wishlistitem",
            constraint=models.UniqueConstraint(
                fields=("wishlist", "product"), name="unique_wishlist_product"
            ),
        ),
    ]
