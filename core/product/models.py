from django.db import models


class Movie(models.Model):
    title = models.CharField(
        'Название',
        max_length=150
    )
    description = models.TextField(
        'Описание'
    )
    release_date = models.DateField(
        'Дата премьеры'
    )
    production_year = models.DateField(
        'Год производства'
    )
    rating = models.PositiveSmallIntegerField(
        'Рейтинг фильма'
    )
    duration = models.CharField(
        'Продолжительность',
        max_length=30
    )
    poster = models.ImageField(
        'Постер',
        upload_to='media/poster_image/'
    )
    movie = models.FileField(
        'Фильм',
        upload_to='media/movie_film/',
        blank=True,
        null=True
    )
    series = models.ManyToManyField(
        'Series',
        blank=True
    )
    categories = models.ManyToManyField(
        'Category',
    )
    genres = models.ManyToManyField(
        'Genre',

    )
    country = models.CharField(
        'Страна производства',
        max_length=150
    )
    age_rating = models.CharField(
        'Возрастной рейтинг',
        max_length=10
    )
    budget = models.PositiveIntegerField(
        'Бюджет',
        default=0
    )
    film_crews = models.ManyToManyField(
        'FilmCrew',
        related_name='movies',
        blank=True
    )
    is_active = models.BooleanField(
        'Активен',
        default=True
    )
    created_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class Series(models.Model):
    number = models.CharField(
        'Номер серии',
        max_length=50
    )
    series = models.FileField(
        'Сериалы',
        upload_to='media/series/'
    )

    # Связь с FilmCrew
    film_crews = models.ManyToManyField(
        'FilmCrew',
        related_name='series',
        blank=True
    )

    def __str__(self):
        return f"Серия {self.number}"

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'


class Category(models.Model):
    title = models.CharField(
        'Категория',
        max_length=100
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    title = models.CharField(
        'Жанр',
        max_length=100
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class FilmCrew(models.Model):
    name = models.CharField(
        'Имя',
        max_length=150
    )
    birth_date = models.DateField(
        'Дата рождения'
    )
    birthplace = models.CharField(
        'Место рождения',
        max_length=150
    )
    image = models.ImageField(
        upload_to='media/film_crew_img/',
        blank=True,
        null=True
    )
    position = models.CharField(
        'Роль в фильме',
        max_length=100
    )
    genres = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Съемочная группа'
        verbose_name_plural = 'Съемочная группа'



















