
class RegistraMudancasMixin:
    '''
        Mantém a propriedade _previous que mantem a versão anterior do dado antes de salvar.
        Também mantem a propriedade changes, que verifica quais mudanças ocorreram:
        self.changes = { 'field' : { 'from': 'versao_anterior, 'to':'nova_versao' } }
        também fornece as propriedades adding e updating
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._previous = self.__dict__.copy()
        self._previous.pop('_state', None)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._previous = self.__dict__.copy()
        self._previous.pop('_state', None)
    
    
    @property
    def changes(self):
        changes = {}
        fields = []
        for field in self._meta.concrete_fields:
            if not field.primary_key:
                fields.append(field.name)

                if field.name != field.attname:
                    fields.append(field.attname) 
        for field in fields:
            if field in self.__dict__.keys() and field in self._previous.keys():
                if self.__dict__[field] != self._previous[field]:
                    changes[field] = {
                        'from': self._previous[field],
                        'to': self.__dict__[field]
                    }
 
        return changes

    @property
    def adding(self):
        '''
            Retorna True se o objeto ainda não foi salvo no banco de dados.
        '''
        return self._state.adding
    @property    
    def updating(self):
        '''
            Retorna True se não é novo objeto.
        '''
        return not self.adding

class ValidateOnSaveMixin:
    '''
        Força o uso do metodo .full_clean()
        e garante que a validação do model sempre vai ser feita
    '''
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
