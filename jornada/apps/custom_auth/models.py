from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UnicodeUsernameValidator
from django.apps import apps
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    """Necessária para que o Django saiba como 'trabalhar'
    com a classe UserProfile
    """

    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, username, password, email=None):
        """Cria um novo objeto 'user profile' """
        if not username:
            raise ValueError('O nome do usuário deve ser preenchido')

        if not password:
            raise ValueError('A senha deve ser preenchida')

        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, email=None):
        """Cria e salva um novo superusuário"""

        user = self.create_user(username, password, email)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


# Custom USER

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ''' 
    Esta class sobrescreve o usuário default do Django
    '''
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
    )

    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    change_password = models.BooleanField(default=True, verbose_name="Forçar alteração de senha")
    date_joined = models.DateTimeField(("date joined"), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def clean(self):
        username = self.username
        if get_user_model().objects.filter(username__iexact=username).exclude(pk=self.pk).exists():
            raise ValidationError({'username': 'Este nome de usuário já existe'}, code='unique')
        
        return super().clean()

    
    def __str__(self):
        return self.username
