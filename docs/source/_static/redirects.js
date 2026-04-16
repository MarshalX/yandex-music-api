// Шим для обратной совместимости старых URL-документации.
// Поддерживает два слоя:
//  1) Якорные редиректы: #yandex_music.Track → dedicated-страница.
//  2) Page-level редиректы: module.html → models.html.
//
// Карты данных формируются docs/generate_client_docs.py и лежат в _static/redirects_map.js.
(function () {
    var anchorMap = window.__YM_REDIRECTS__;
    var pageMap = window.__YM_PAGE_REDIRECTS__;

    // 1) Якорный редирект: приоритетно, т.к. ссылка может указывать на
    //    существующую страницу с устаревшим якорем.
    if (anchorMap) {
        var hash = window.location.hash.slice(1);
        if (hash && !document.getElementById(hash)) {
            var anchorTarget = anchorMap[hash];
            if (anchorTarget) {
                window.location.replace(anchorTarget);
                return;
            }
        }
    }

    // 2) Page-level редирект: сравниваем имя html-файла текущего пути.
    if (pageMap) {
        var path = window.location.pathname;
        var fileName = path.substring(path.lastIndexOf('/') + 1);
        var pageTarget = pageMap[fileName];
        if (pageTarget) {
            window.location.replace(pageTarget);
        }
    }
})();
