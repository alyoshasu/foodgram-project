from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Ingredient(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    dimension = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="ед. изм.",
    )
    # quantity = models.IntegerField()

    def __str__(self):
        return self.title


class Recipe(models.Model):
    BREAKFAST = 'BR'
    LUNCH = 'LN'
    DINNER = 'DN'
    TAG_CHOICES = [
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    ]
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    image = models.ImageField(
        upload_to="recipes/static/images/uploads/",
        verbose_name="Картинка",
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингредиенты",
    )
    tag = models.CharField(
        max_length=2,
        choices=TAG_CHOICES,
        default=DINNER,
        verbose_name="Тег",
    )
    time = models.IntegerField(
        verbose_name="Время приготовления, мин",
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )

    def is_tag(self):
        return self.tag in {
            self.BREAKFAST,
            self.LUNCH,
            self.DINNER,
        }

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
