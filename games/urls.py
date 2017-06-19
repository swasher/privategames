from django.conf.urls import url
from games import views

urlpatterns = [
    url(r'^$', views.hello, name='hello'),
    url(r'^games/$', views.games, name='games'),
    url(r'^cabinet/$', views.cabinet, name='cabinet'),
    url(r'^search/$', views.search, name='search'),
    url(r'^add_game/(?P<igdb_id>\d+)/$', views.add_game, name='add_game'),
    url(r'^tags/$', views.tags, name='tags'),
    url(r'^toggle_tag/$', views.toggle_tag, name='toggle_tag'),
    url(r'^game/(?P<pk>\d+)/$', views.game_change, name='game'),
    url(r'^delete_game/$', views.delete_game, name='delete_game'),
    url(r'^delete_tag_ajax/$', views.delete_tag_ajax, name='delete_tag_ajax'),
    url(r'^add_tag_ajax/$', views.add_tag_ajax, name='add_tag_ajax'),
]