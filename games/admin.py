from django.contrib import admin
from django.contrib.auth.models import User
# from django.conf import settings
# User = settings.AUTH_USER_MODEL

from .models import Game
from .models import Tag


admin.site.site_header = 'Private Games'

# class CollectionAdmin(admin.ModelAdmin):
#     def get_field_queryset(self, db, db_field, request):
#         """
#         If the ModelAdmin specifies ordering, the queryset should respect that
#         ordering.  Otherwise don't specify the queryset, let the field decide
#         (returns None in that case).
#
#         Фильтрация тегов, показываются только теги залогиненого юзера
#         Надо ли оно? Ведь админ-интерфейсом обычные юзеры не пользуются
#
#         """
#         if db_field.name == 'tags':
#
#             # tags = int(request.resolver_match.args[0])
#
#             return db_field.remote_field.model._default_manager.filter(
#                 user=request.user
#             )
#
#         super().get_field_queryset(db, db_field, request)



# class GamesInline(admin.TabularInline):
#     model = Game
#     extra = 0
#
#
# class GameAdmin(admin.ModelAdmin):
#     pass
#
# class UserAdmin(admin.ModelAdmin):
#     pass


# admin.site.register(Game, GameAdmin)
# admin.site.register(Tag)
# admin.site.register(User, UserAdmin)
