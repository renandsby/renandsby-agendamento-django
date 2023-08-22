from django.db.models import Q
from datetime import datetime
import random

def logica_adolescente(adol):
    adol.sipia = None if adol.sipia == "" else adol.sipia
    adol.cpf = None if adol.cpf == "" else adol.cpf
    adol.cnh = None if adol.cnh == "" else adol.cnh
    
    if adol.adding:
        random.seed(datetime.now().timestamp())
        _id_jornada = str(random.randint(100001,999999))
        while adol.__class__.objects.filter(id_jornada=_id_jornada).exists():
            random.seed(datetime.now().timestamp())
            _id_jornada = str(random.randint(100001,999999))
        
        adol.id_jornada = _id_jornada





def logica_principal(obj):
    '''    
       Garante que o adolescente não possui mais de um relacionado principal.
       Caso já exista um principal anterior, este anterior é desmarcado (principal=False)
       Esta função deve ser usada no método clean
    '''
    if hasattr(obj, 'principal') and hasattr(obj, 'adolescente'):
        principal_anterior = obj.__class__._default_manager.filter(
            ~Q(id=obj.id), # pra nao trazer o mesmo objeto
            adolescente= obj.adolescente_id,
            principal=True,
            )
        
    
        if not principal_anterior.exists() and not obj.principal:
            obj.principal = True

        if obj.principal and principal_anterior.exists():
            if obj != principal_anterior:
                principal_anterior.update(principal=False)
    
            

       