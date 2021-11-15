import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Product, Parcel
from .utils import get_id_data


@receiver(post_delete, sender=Product)
def update_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Product` object is deleted.
    """

    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Product` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Product.objects.get(pk=instance.pk).image
    except Product.DoesNotExist:
        return False

    new_file = instance.image

    if not old_file == new_file:
        if old_file.path:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)


@receiver(post_delete, sender=Product)
def update_parcels_on_delete(sender, instance, **kwargs):
    """
    Deletes product from parcel
    when corresponding `Product` object is deleted.
    """

    parcels = Parcel.objects.all()
    parcels_id = get_id_data(parcels)
    product_id = str(instance.id)

    for pid in parcels_id:
        parcel = Parcel.objects.filter(id=pid)

        for data in parcel.values():
            items_list = data['items'].split(',')

            if product_id in items_list:
                items_list.remove(product_id)
                new_products = ",".join(items_list)
                Parcel.objects.filter(id=pid).update(items=new_products)
