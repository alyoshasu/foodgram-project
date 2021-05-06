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

        }
    )


def project(request):
    return render(
        request,
        "about.html",
        {
            "title": "О проекте",

        }
    )
