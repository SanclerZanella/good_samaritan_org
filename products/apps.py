from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Checkout app configuration
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        """
        Overwrite ready function to connect
        the checkout signals
        """
        import products.signals
