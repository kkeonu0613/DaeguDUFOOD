from django.apps import AppConfig

class RestaurantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurants'  # ���ø����̼��� �̸�

    def ready(self):
        import restaurants.signals  # ��ȣ�� ����Ʈ
