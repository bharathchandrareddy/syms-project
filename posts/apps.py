from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'posts'
    verbose_name = 'Posts,Likes,Comment'  #this creates a order in admin site
    # take this PostsConfig to __init__.py file and add it over there