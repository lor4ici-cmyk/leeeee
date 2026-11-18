# Leeeee

Публичная страница: https://lor4ici-cmyk.github.io/leeeee/

1. Обнови `profile.json` и добавь нужные медиа в `uploads/` или `assets/`.
2. Запусти `python3 scripts/update-page.py`: команда обновит превью ссылки, резервный HTML и версии JS/CSS.
3. Проверь сайт через `python3 -m http.server 8000` и опубликуй изменения в `main`.

`editor.html` — отдельная точка входа для среды с серверным API. GitHub Pages не выполняет `api/*`; для редактирования на Pages используй `profile.json`. Серверная часть здесь не хранится. Не коммить файлы авторизации или секреты.
