from django.urls import path
from.views import post_view,like_post,PostDeleteView,PostUpdateView

app_name = 'posts'
urlpatterns = [
    path('',post_view,name='main-post-view'),
    path('liked/',like_post,name='main-like-view'),
    path('<pk>/update/',PostUpdateView.as_view(),name='post-update'),  # the names can be used in html forms in href links
    path('<pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
]
