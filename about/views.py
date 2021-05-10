from django.shortcuts import render


def author(request):
    return render(
        request,
        "about.html",
        {
            "title": "Об авторе",
            "text": "Алексей Сухачевский (t: @alyoshasu)"
        }
    )


def technologies(request):
    return render(
        request,
        "about.html",
        {
            "title": "Технологии",
            "text": "Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации "
                    "других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в "
                    "магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких "
                    "выбранных блюд."
        }
    )


def project(request):
    return render(
        request,
        "about.html",
        {
            "title": "О проекте",
            "text": "Django, gunicorn, PostgreSQL, nginx, Docker, Django REST Framework, Github Actions, Яндекс.Облако"
        }
    )
