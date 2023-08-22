from rest_framework.utils import model_meta
from .utils import update_multiple_data, save_with_parent_serializer
from rest_framework import serializers


def create_nested_reverse(func):
   
    def wrapper(self, *args, **kwargs):
        validated_data = None
        instance = None

        if func.__name__ == 'create':
            validated_data = args[0]
        if func.__name__ == 'update':
            instance = args[0]
            validated_data = args[1]

        if not hasattr(self.Meta, 'reverse_related_field'):
            self.Meta.reverse_related_field = self.Meta.model.__name__.lower()
        

        ModelClass = self.Meta.model
        model_field_info = model_meta.get_field_info(ModelClass)
        reverse_related = {x:model_field_info.relations[x] for x in model_field_info.relations if model_field_info.relations[x].reverse == True}

        related_data = {}

        for field in self._writable_fields:
            if field.source in validated_data and field.source in reverse_related:      
                related_data[field.source] = self.context['request'].data.get(field.source, None)
                validated_data.pop(field.source, None)

        instance = func(self, *args, **kwargs)


        for x in reverse_related:
             if x in related_data and related_data[x] is not None:
                if type(related_data[x]) is not list:
                    related_data[x] = [related_data[x]]
                
                related_model_info = model_meta.get_field_info(reverse_related[x].related_model)
                update  = {}
                for key in related_model_info.relations:
                    if related_model_info.relations[key].related_model == ModelClass:
                        update = {key : instance.id}

                if not update:
                    update = {self.Meta.reverse_related_field : instance.id}                    
                
                data = update_multiple_data(related_data[x], **update)
                save_with_parent_serializer(data, serializer = self, related_name = x, action = func.__name__)

        return instance

    return wrapper


class WritableNestedSerializer(serializers.ModelSerializer):
    '''
        Serializer que implementa o metodo create_nested_reverse nos métodos create e update.
        Permite que se crie e atualize um objeto e em seguida crie objetos relacionados em uma só requisição
        
        Ex: Você pode criar ou atualizar um adolescente e em seguida adicionar a lista de telefones dele. 
        Note que NÃO é possível atualizar um telefone, apenas adicionar telefones novos. Neste exemplo, para
        atualizar um telefone seria necessário utilizar o endpoint /api/adolescente/<id>/telefone/<id>/

        -> (opcional) colocar no Meta o campo reverse_related_field  Ex: reverse_related_field = 'adolescente'

         O formato de POST esperado:
        {
            nome: 'nome',
            nome_mae: 'nome_mae',
            telefones: [
                    {
                        numero: '123456789',
                        descricao: 'residencial',
                        principal: True
                    },
                    {
                        numero: '987654321',
                        descricao: 'comercial'
                    }
                ]
        }
            
    '''
    
    @create_nested_reverse
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @create_nested_reverse
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

class ChoiceField(serializers.ChoiceField):
    
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return { 
                "id" : obj, 
                "descricao" : self._choices[obj] 
                }

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)
        


class DynamicFieldsDepthExcludeSerializer(serializers.ModelSerializer):
    """
        Um ModelSerializer que checa nos parametros passado na request pelos campos:
        'fields' que são os campos para mostrar
        'exclude' que são os campos para excluir
        'depth' que é a profundidade dos campos de chave estrangeira
    """

    def __init__(self, *args, **kwargs):
        
        super(DynamicFieldsDepthExcludeSerializer, self).__init__(*args, **kwargs)

        request = self.context.get('request', False)
        
        if request:
            fields = request.query_params.get('fields', False)
            exclude = request.query_params.get('exclude', False)
            depth = request.query_params.get('depth', False)
            
            if depth:
                self.Meta.depth = int(depth) if request.method == 'GET' else 0
            else:
                self.Meta.depth = 1 if request.method == 'GET' else 0
                
                
            if fields:
                fields = fields.split(',')
                allowed = set(fields)
                existing = set(self.fields.keys())
            
                for field_name in existing - allowed:
                    self.fields.pop(field_name)
            
            if exclude:
                exclude = exclude.split(',' )
                for field_name in exclude:
                    self.fields.pop(field_name)