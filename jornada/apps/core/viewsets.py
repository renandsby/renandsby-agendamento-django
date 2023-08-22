from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
import re

from .mixins import TrapDjangoValidationErrorCreateMixin, TrapDjangoValidationErrorUpdateMixin

from .utils import update_multiple_data, save_with_parent_serializer


class BaseModelViewSet(TrapDjangoValidationErrorUpdateMixin,
                         TrapDjangoValidationErrorCreateMixin,
                         viewsets.ModelViewSet):
    '''
        Viewset que resolve o problema das Exceptions levantadas pelo Django e pelo Rest Framework
        serem diferentes (ambas chamadas ValidationError), passando por esse Viewset fica garantido
        que ambos serão do tipo ValidationError do DRF
    '''
    pass
    



class ArquivosNoFormViewSet(BaseModelViewSet):
    '''
        Implementa os metodos create e update para aceitar a criação de lista de dados 
        relacionados junto com o objeto num único POST.
        Esse ViewSet é especificamente para criação de objetos junto com relacionados que possuam arquivos binários, 
        utilizando apenas um POST no formato de multipart-form, pode-se criar o objeto e seus relacionados
        
        Se você quiser por exemplo criar um processo junto com anexos, 
        basta colocar nos dados do formulario:
        numero_processo = numero_processo
        anexos_1_anexo = <file>
        anexos_1_descricao = descricao
        anexos_2_anexo = <file>
        anexos_2_descricao = descricao
        etc...
        
        
        por fim isso irá criar os objetos Anexo com seus atributos, e ligar eles ao processo criado no POST.
        IMPORTANTE: essa forma de criação de relacionados NÃO PERMITE UPDATE apenas criação.
        Se por exemplo você quiser atualizar um anexo já criado, você precisa fazer um PUT em /processos/<id>/anexos/<id>        
        
    '''
     
    def save_files(self, request, serializer, *args, **kwargs):
        for related_name in self.arquivos_no_form_fields:

            file_dict = {}
            for key in request.data:
                match = re.match(related_name+'_[\d]', key) # string possui anexos_x ? (x sendo um número)
                
                if match and key.startswith(match.group(0)): # se possui, a string começa com anexos_x?
                    if match.group(0) not in file_dict:
                        file_dict[match.group(0)] = {} # cria uma entrada no dict anexos pro anexos_x se nao existir
                    
                    file_key = re.split(related_name+'_[\d]', key)[1][1:] # pega o que tem depois de anexos_x_ para usar de chave"
                    file_dict[match.group(0)][file_key] = request.data[key]

            '''
            Nesse ponto vai existir uma lista nor formato:
                file_dict = {
                    'anexos_1': {
                        'anexo': <InMemoryUploadedFile: DSC00248.jpg (image/jpeg)>}
                        'oficio': 'true', 
                        'tipo': 'Memorando', 
                    },
                }    
            '''    
            if file_dict:

                instance = serializer.Meta.model.objects.get(id=serializer.data['id'])
                related_fk = getattr(instance, related_name).field.name
                update = {related_fk: instance.id}	  
                
                file_data = update_multiple_data(file_dict.values(), **update)
                save_with_parent_serializer(file_data, serializer, related_name = related_name)
        
        
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.save_files(request, serializer)
        
        # força uma buscar no banco de novo pra virem os anexos no retorno no POST
        serializer = serializer.__class__(serializer.Meta.model.objects.get(id=serializer.data['id']))
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        self.save_files(request, serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
            
        #forca a buscar no banco de novo pra virem os anexos no retorno no POST
        serializer = serializer.__class__(serializer.Meta.model.objects.get(id=serializer.data['id']))

        return Response(serializer.data)