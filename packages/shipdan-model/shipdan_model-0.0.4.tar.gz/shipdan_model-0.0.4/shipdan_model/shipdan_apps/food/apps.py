from django.apps import AppConfig


class FoodModelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shipdan_apps.food'
    label = 'food_model'
