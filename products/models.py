from django.db import models


class Category(models.Model):
    """
    Category Model

    Attributes:
        *name: A string indicating the category name;
        *friendly_name: A string indicating category friendly name.

    Sub-classes:
        *Display the object's plural name.

    Methods:
        *__str__: Display the object's headline in the admin interface,
                        it returns a nice, human-readable representation of
                        the model;
        *get_friendly_name: Display the object's friendly name.
    """

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    """
    Product Model

    Attributes:
        *sku: Stock Keeping Unit alphanumeric code;
        *name: A string indicating product name;
        *description: A text indicating product description;
        *f_parcel: A sequence of numbers in text formating
                   indicating in which family parcels the product
                   is included;
        *m_needed: A boolean field indicating if the product is
                   urgent;
        *price: A decimal number indicating product price;
        *image_url: A url pointing to image resource hosted in
                    another cloud platform;
        *image: Image file name and extension in root directory.

    Methods:
        *__str__: Display the object's headline in the admin interface,
                        it returns a nice, human-readable representation of
                        the model.
    """

    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    m_needed = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to='products/items/')

    def save(self, *args, **kwargs):
        """
        Override the original save method to remove
        any suffix equal to the parcel sku suffix.
        """

        product_sku = self.sku
        suffix = product_sku.split('_')[-1]

        if suffix == 'pc':
            self.sku = product_sku.split('_')[0]
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Parcel(models.Model):
    """
    Parcel Model

    Attributes:
        *sku: Stock Keeping Unit alphanumeric code;
        *name: A string indicating parcel name;
        *description: A text indicating parcel description;
        *price: A decimal number indicating parcel price;
        *image_url: A url pointing to image resource hosted in
                    another cloud platform;
        *image: Image file name and extension in root directory.

    Methods:
        *__str__: Display the object's headline in the admin interface,
                        it returns a nice, human-readable representation of
                        the model.
    """

    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    items = models.TextField()
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to='products/items/')

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the
        suffix to the parcel sku.
        """

        parcel_sku = self.sku
        suffix = parcel_sku.split('_')[-1]

        if suffix == 'pc':
            super().save(*args, **kwargs)
        else:
            self.sku = f'{self.sku}_pc'
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name
