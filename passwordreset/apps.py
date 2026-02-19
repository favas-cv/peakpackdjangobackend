from django.apps import AppConfig


class PasswordresetConfig(AppConfig):
    name = 'passwordreset'
    
    def ready(self):
        import passwordreset.signals
