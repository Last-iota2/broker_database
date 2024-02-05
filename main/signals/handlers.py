from testsite import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from browse.models import Receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_receiver_for_new_user(sender, **kwargs):
  if kwargs['created']:
    Receiver.objects.create(user=kwargs['instance'])