// Шим для обратной совместимости старых URL-закладок.
// После переноса документации классов в подпакеты (yandex_music.artist.artist.Artist),
// старые anchor-ссылки вида yandex_music.html#yandex_music.Track больше не существуют.
// Этот скрипт ловит такие переходы и редиректит на каноническую страницу.
(function () {
    var map = window.__YM_REDIRECTS__;
    if (!map) return;

    var hash = window.location.hash.slice(1);
    if (!hash) return;

    // Если якорь есть на текущей странице — ничего не делаем.
    if (document.getElementById(hash)) return;

    var target = map[hash];
    if (target) {
        window.location.replace(target);
    }
})();
