from django.apps import AppConfig
from django.db.models.signals import post_save
from django.db.models.signals import pre_save


from django.apps import apps



class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals

    # def ready(self):
    #     # importing model classes
    #     from .models import Blog  # or...
    #     MyModel = self.get_model('Blog')

    #     # registering signals with the model's string label
    #     pre_save.connect(receiver, sender='app_label.core')

