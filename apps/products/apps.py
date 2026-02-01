from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"

    def ready(self):
        """앱 초기화 시 signals 등록"""
        import apps.products.signals  # noqa
