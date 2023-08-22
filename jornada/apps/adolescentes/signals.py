from django.db.models.signals import pre_save
from django.dispatch import receiver
from adolescentes.models import Adolescente


@receiver(pre_save, sender=Adolescente)
def trata_homonimos(sender, instance, **kwargs):

    if instance.checa_homonimo:   
        homonimos = Adolescente._default_manager.filter(
            nome__iexact = instance.nome,
            checa_homonimo = True
        )
        
        if instance.pk:
            homonimos = homonimos.exclude(pk=instance.pk)
        
        if homonimos.exists():
            instance.possui_homonimo = True
            homonimos.update(possui_homonimo = True)

