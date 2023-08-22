from django.db.models.signals import post_save
from django.dispatch import receiver
from livro.models import Livro


@receiver(post_save, sender=Livro)
def copia_efetivo_criacao(sender, instance, created, **kwargs):
    if created:
        instance.copia_efetivo_criacao()