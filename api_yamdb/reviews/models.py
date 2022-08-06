from django.db import models

from django.db.models.constraints import UniqueConstraint

from django.core.validators import MinValueValidator, MaxValueValidator

from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='категория')
    slug = models.SlugField(unique=True, verbose_name='slug категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='жанр')
    slug = models.SlugField(unique=True, verbose_name='slug жанра')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='произведение', db_index=True
    )
    year = models.IntegerField(
        verbose_name='год выпуска',
        blank=True, null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles',
        blank=True, null=True, verbose_name='категория',
        db_index=True
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles', verbose_name='жанр',
        db_index=True
    )
    description = models.TextField(
        verbose_name='описание', blank=True, null=True
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class Review(models.Model):

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews")
    text = models.TextField("Текст отзыва")
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(10)],
                                             default=0)
    pub_date = models.DateTimeField(
        "Дата и время публикации отзыва",
        auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        constraints = (
            UniqueConstraint(
                fields=('author', 'title',), name='unique_review'
            ),
        )


class Comment(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="comments")
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments")
    text = models.TextField("Текст комментария")
    pub_date = models.DateTimeField(
        "Дата и время публикации комментария",
        auto_now_add=True
    )
