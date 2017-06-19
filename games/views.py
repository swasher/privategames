import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Count
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from igdb.requester import Requester
from igdb import Filter
from igdb import operators
from igdb.operators import EQ, PREFIX

from .forms import GameForm
# from .forms import NewTagForm
from .models import Game
from .models import Tag


def hello(request):
    return render(request, 'hello.html')


@login_required()
def cabinet(request):
    return render(request, 'cabinet.html')



@login_required
def search(request):

    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            search_string = form.cleaned_data['game']
            igdb_api_key = settings.IGDB_API_KEY
            req = Requester(igdb_api_key)
            fields = 'name,storyline,cover,summary,popularity,first_release_date'
            #filter = Filter(field='name', operator=operators.EQ, value=search_string)
            #filtr_platform = Filter(field='release_dates.platform', operator=operators.EQ, value='6') # not working
            filter_name = Filter(field='name', operator=PREFIX, value=search_string) # not good due register-depended searching
            dump = req.get_games(fields=fields,
                                 limit=20,
                                 offset=0,
                                 order='popularity:desc',
                                 search=search_string,
                                 #filters = [filter_name]
                                 )

            # Поиск слишком широкий, ищет не только по названиям, а полнотестово.
            # Отсеиваем те, в названиие которых нет искомой строки search_string
            response = [i for i in dump if search_string.lower() in i['name'].lower()]

            existing_games = list(Game.objects.filter(user=request.user).values_list('igdb_id', flat=True))

            for i, game in enumerate(response):

                # Convert Unix-epoch date (int) to python datetime object
                try:
                    game['first_release_date'] = datetime.datetime.fromtimestamp(game['first_release_date']/1000)
                except KeyError:
                    game['first_release_date'] = None

                if game['id'] in existing_games:
                    response[i]['exist'] = True
                try:
                    game['cover_url'] = 'https://images.igdb.com/igdb/image/upload/t_{size}/{hash}.jpg'.format(size='thumb', hash=game['cover']['cloudinary_id'])
                except KeyError:
                    pass
    else:
        form = GameForm()
        response = None

    return render(request, 'search.html', {'form':form, 'games':response})


@login_required
def games(request):
    user = request.user
    #collection = Collection.objects.filter(user=user)

    if 'filter' in request.GET and request.GET['filter'] == 'tag':
        game_list = Game.objects.filter(user=user, tag__pk=request.GET['pk'])
    else:
        game_list = Game.objects.filter(user=user)

    paginator = Paginator(game_list, 8)  # Show 6 games per page
    page = request.GET.get('page', 1)

    try:
        games = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        games = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        games = paginator.page(paginator.num_pages)

    return render(request, 'games.html', {'games': games})


@login_required
@ensure_csrf_cookie
def add_game(request, igdb_id):

    if not Game.objects.filter(igdb_id=igdb_id).exists():

        game = Game()
        game.igdb_id = igdb_id
        game.user = request.user
        game.date_add = datetime.datetime.now()
        game.save()

    return redirect('/game/{}'.format(game.id))


@login_required
def game_change(request, pk):
    game = Game.objects.get(pk=pk)

    # Получаем список тегов, присвоенных данной игре: <QuerySet ['tag2', 'tag5']>
    active_tag_list = list(Tag.objects\
        .filter(user=request.user, games=game)\
        .values_list('name', flat=True))
        # .values_list('name', 'active')
        # .annotate(active=Count('games'))\

    # Получаем список всех тегов юзера в виде списка кортежей: <QuerySet [{'active': 2, 'name': 'tag2', 'pk': 11}, {'active': 1, 'name': 'tag5', 'pk': 4}]>
    # Каждый кортеж содержит имя pk, имя тега и кол-во игр с данным тегом
    tag_list = Tag.objects\
        .filter(user=request.user) \
        .annotate(total=Count('games'))\
        .values('pk', 'name', 'total')

    for tag in tag_list:
        if tag['name'] in active_tag_list:
            tag['active'] = True
        else:
            tag['active'] = False

    return render(request, 'game.html', {'game': game, 'tags': tag_list})





@login_required
@ensure_csrf_cookie
def delete_game(request):
    """
    AJAX
    """
    if request.is_ajax() and request.method == u'POST':
        POST = request.POST
        if 'game_pk' in POST:
            pk = int(POST['game_pk'])

            # TODO тут у нас небольшой быдлокод:
            # except без укзания эксепшенов
            # при возникновении эксепшена статус failed никак не обрабатывается
            # можно, например, при неудачном удалении редирктить на страницу игры


            # Сначала удаляем связь между игрой и юзером
            #
            try:
                game = Game.objects.get(pk=pk)
                assigned_game = Ownership.objects.get(user=request.user, game=game)
            except [Game.DoesNotExist, Ownership.DoesNotExist]:
                pass
                #TODO возвратить на страницу игры
            else:
                assigned_game.delete()
                messages.add_message(request, messages.INFO, "Game '{}' delete success".format(game.name))



            try:
                g = Game.objects.get(pk=pk)
                title = g.name
                Game.objects.get(pk=pk).delete()
                messages.add_message(request, messages.INFO, "Game '{}' delete success".format(title))
            except:
                status = 'failed'
            else:
                status = 'sucess'

            results = {'redirect': '/games/', 'status': status}
            return JsonResponse(results)


@login_required
def tags(request):
    tag_list = Tag.objects.all().filter(user=request.user)
    return render(request, 'tags.html', {'tags': tag_list})


@login_required
@ensure_csrf_cookie
# AJAX
def toggle_tag(request):
    if request.is_ajax() and request.method == u'POST':
        POST = request.POST
        if 'tag_pk' in POST and 'game_pk' in POST:
            tag_pk = int(POST['tag_pk'])
            game_pk = int(POST['game_pk'])
            tag = Tag.objects.get(pk=tag_pk)
            game = Game.objects.get(pk=game_pk)

            if Tag.objects.filter(games=game, pk=tag_pk).exists():
                tag.games.remove(game)
                results = {'status': 'sucess_remove'}
                return JsonResponse(results)
            else:
                tag.games.add(game)
                results = {'status': 'sucess_add'}
                return JsonResponse(results)

@login_required
@ensure_csrf_cookie
def delete_tag_ajax(request):
    """
    AJAX
    """
    if request.is_ajax() and request.method == u'POST':
        POST = request.POST
        results = {}
        tag_name = 'default'

        if 'pk' in POST:
            pk = int(POST['pk'])

            try:
                tag = Tag.objects.get(pk=pk)
                tag_name = tag.name
                if not Game.objects.filter(tag=tag).exists():
                    messages.add_message(request, messages.INFO, "Tag `{}` delete success".format(tag_name))
                    #messages.success(request, "The object has been modified.")
                    tag.delete()
                    status = 'sucess'
                else:
                    messages.add_message(request, messages.INFO, "Tag `{}` has games!".format(tag_name))
                    #messages.error(request, "The object was not modified.")
                    status = 'exist'
            except:
                status = 'failed'

            results = {'status': status, 'name': tag_name}

        return JsonResponse(results)


@login_required
@ensure_csrf_cookie
def add_tag_ajax(request):
    """
    AJAX
    """
    # if request.is_ajax() and request.method == u'POST':
    if request.method == u'POST':
        POST = request.POST
        tagpk = None
        results = {}

        if 'tag_name' in POST:
            tag_name = str(POST['tag_name'])

            try:
                if not Tag.objects.filter(name=tag_name).exists():
                    tag = Tag.objects.create(name=tag_name, user=request.user)
                    tag.save()
                    messages.add_message(request, messages.INFO, 'tag {} creating success'.format(tag_name))
                    status = 'sucess'
                    tagpk = tag.pk
                else:
                    messages.add_message(request, messages.WARNING, 'tag {} already exist'.format(tag_name))
                    status = 'exist'
            except:
                status = 'failed'

            results = {'status': status, 'name': tag_name, 'tagpk': tagpk}

            return JsonResponse(results)

    else:
        results = {'status': 'non-ajax', 'name': None}
        return JsonResponse(results)