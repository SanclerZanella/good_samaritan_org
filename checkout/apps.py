from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """
    Checkout app configuration
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        """
        Overwrite ready function to connect
        the checkout signals
        """
        import checkout.signals
