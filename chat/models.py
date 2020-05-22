from django.db import models
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager

from stdimage.models import StdImageField

from .consumers import ChatConsumer

import uuid

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename

class UserManager(BaseUserManager):
    """
    Gerenciador de usuarios da classe customizada de usuarios
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório!')
        email = self.normalize_email(email) # retira caracteres especiais e joga tudo em caixa baixa
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is False:
            raise ValueError('SuperUser precisa ter is_superuser=True.')

        if extra_fields.get('is_staff') is False:
            raise ValueError('SuperUser precisa ter is_staff=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField("E-mail", max_length=254, unique=True)
    is_staff = models.BooleanField("Membro de Equipe", default=True)
    perfil_image = StdImageField('Foto do Perfil', upload_to=get_file_path, 
                                    variations={
                                        'thumb': 
                                                {
                                                    'width': 480,
                                                    'height': 480,
                                                    'crop': True
                                                }
                                    })

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return self.email
    
    object = UserManager()


class LoggedUser(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    status = models.CharField(max_length=30, default='active')
    perfil_image = models.CharField(max_length=300, default='')
    logged_at = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.username

def login_user(sender, request, user, **kwargs):
    user_logged = LoggedUser(username=user.username)
    user_logged.status = 'online'
    user_logged.perfil_image = user.perfil_image
    print(f'Perfil Image on Login: {user_logged.perfil_image}')
    user_logged.save()
    usuarios_logados()
    

def logout_user(sender, request, user, **kwargs):
    try:
        u = LoggedUser.objects.get(pk=user.username)
        u.delete()
        usuarios_logados()
    except LoggedUser.DoesNotExist:
        pass


def usuarios_logados():
    usuarios_logados = LoggedUser.objects.all()
    print(f'Usuarios logados no Django: {usuarios_logados}')


user_logged_in.connect(login_user)
user_logged_out.connect(logout_user)
