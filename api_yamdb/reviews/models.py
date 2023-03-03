from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.PositiveIntegerField('Год выпуска')
    description = models.TextField('Описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name='Категория',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        blank=True,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name[:15]


class Review(models.Model):
    """Модель для Отзывов"""
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    score = models.IntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comment(models.Model):
    """Модель для Комментариев"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='Comments',
        verbose_name='Отзыв'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
