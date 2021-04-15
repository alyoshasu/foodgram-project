from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name="Название",
    )
    dimension = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="ед. изм.",
    )

    def __str__(self):
        return '{}, {}'.format(self.title, self.dimension)


class Tag(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Название",
    )

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    title = models.CharField(
        max_length=256,
        verbose_name="Название",
    )
    image = models.ImageField(
        upload_to="recipe/",
        verbose_name="Картинка",
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингредиенты",
        through='IngredientRecipe',
        related_name="recipes",
    )
    tags = models.ManyToManyField(
        Tag,
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

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ["-pub_date"]


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField()

    def __str__(self):
        return '{} {} - {} в {}'.format(self.quantity, self.ingredient.dimension, self.ingredient.title, self.recipe.slug)

    class Meta:
        unique_together = ['recipe', 'ingredient']
