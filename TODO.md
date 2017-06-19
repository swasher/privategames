[]

Known bug:

- При удалении тега, если в этот момент висел message об удалении
предыдущего тега, то время до исчезновения мессаджа не обновляется;
в результете, новый мессадж пропадает практически сразу, в тот же момент,
когда должен был пропасть предыдущий

- При добавлении нового тега, и попытке его немедленного удаления (до
перезагрузки страницы), удаляется тег, первый в списке.

Это просходит по той причине, что мы делает .clone() c параметром
 `deepclone` с первого тега (первого в списке).

Чтобы исправить эту ситуацию, надо курить Event Handler Attachment
http://api.jquery.com/on/

- При вводе первого тега он не появляется, так как отсутствует сам блок с тегами: {% if tags %} ....

Код находится в конце функции `create_tag`

- сделать возможность добавлять свои скриншоты
- сделать возможность добавлять свое видео
- сделать возможность изменять постер
- добавить франшизы

СПИСОК API
- GIANTBOMB
https://www.giantbomb.com/api/

- TGDB
http://wiki.thegamesdb.net/index.php/API_Introduction
https://github.com/alfredocdmiranda/tgdb-api - API простой для фласка, можно взять как образец

- IGDB
https://www.igdb.com/api
у этих картинки хранятся на Cloudinary, так что нет смысла копировать

https://github.com/nuxlic/igdb-api    <-- currently used
https://github.com/noragami/igdbapi

- MOBYGAMES [ALPHA]
http://www.mobygames.com/info/api
чтоб получить доступ, надо писат в пм овнеру: http://www.mobygames.com/forums/dga,2/dgb,4/dgm,231400/