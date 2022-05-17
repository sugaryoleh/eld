from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from eld_admin.models import Driver


@receiver(post_delete, sender=Driver, dispatch_uid='delete_driver_user')
def delete_driver_user(sender, instance, **kwargs):
    User.objects.get(pk=instance.user.id).delete()