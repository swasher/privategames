from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from igdb.requester import Requester
import igdbapi

# ON DELETE CASCADE - вместе с данным объектом удаляются все объекты, внешние ключи которых указывают на данный объект.
class Game(models.Model):
    igdb_id = models.PositiveIntegerField(unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    notice = models.TextField(blank=True, verbose_name='Заметка пользователя')
    date_add = models.DateField(auto_now_add=True)
    date_finish = models.DateField(blank=True, null=True)

    # ??? link = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return str(self.igdb_id)

    @property
    def data(self):
        igdb_api_key = settings.IGDB_API_KEY
        igdbapi.core.APIClient(api_key=igdb_api_key)
        game = igdbapi.games.Games().find(self.igdb_id)
        data = {'name': game.name,
                'cover_small': 'https://images.igdb.com/igdb/image/upload/t_{size}/{hash}.jpg'.
                    format(size='cover_small', hash=game.cover.cloudinary_id),
                'cover_big': 'https://images.igdb.com/igdb/image/upload/t_{size}/{hash}.jpg'.
                    format(size='cover_big', hash=game.cover.cloudinary_id)
                }
        return data


# class User(AbstractUser):
#     games = models.ManyToManyField(Game, through='Ownership')


class Tag(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    games = models.ManyToManyField(Game, blank=True)

    class Meta:
        verbose_name = 'Список'
        verbose_name_plural = 'Списки'
        ordering =['name']

    def __str__(self):
        return self.name


