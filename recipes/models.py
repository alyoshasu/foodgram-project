from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        'Название ингредиента',
        max_length=256,
    )
    dimension = models.CharField(
        'ед. изм.',
        max_length=64,
        blank=True,
    )

    class Meta:
        ordering = ('title', )
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return '{}, {}'.format(self.title, self.dimension)


class Tag(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Title",
    )
    display_name = models.CharField(
        max_length=50,
        verbose_name="Название",
    )
    color = models.CharField(
        max_length=50,
        verbose_name="Цвет",
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
        validators=[MinValueValidator(1)],
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
        return self.title

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
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
    )

    def __str__(self):
        return '{} {} - {} в {}'.format(
            self.quantity,
            self.ingredient.dimension,
            self.ingredient.title,
            self.recipe.slug
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_IngredientRecipe'
            )
        ]
