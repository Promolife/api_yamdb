from django.db import models


class Category(models.Model):
    """ Модель категории произведения."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name[:15]}'


class Genre(models.Model):
    """ Модель жанра произведения."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return f'{self.name[:15]}'


class Title(models.Model):
    """ Модель произведений."""

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    description = models.TextField(
        'Описание произведения',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='genres',
        verbose_name='Жанр'
    )
    name = models.CharField(max_length=256)
    year = models.IntegerField()

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return f'{self.name[:15]}'


class GenreTitle(models.Model):
    """ Модель ManyToMany для связи произведений и жанров."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='genretitle',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titlegenre',
    )

    class Meta:
        models.UniqueConstraint(
            fields=['genre', 'title'],
            name='unique_follow'
        )
