from django.apps import AppConfig

class RestaurantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurants'  # 애플리케이션의 이름

    def ready(self):
        import restaurants.signals  # 신호를 임포트
