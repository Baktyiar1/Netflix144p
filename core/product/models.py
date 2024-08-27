from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Banner(models.Model):
    title = models.CharField(
        'Название',
        max_length=123
    )
    banner_image = models.ImageField(
        'Изображение',
        upload_to='media/banner_image/'
    )
    is_asset = models.BooleanField(
        'Активность',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'



class Movie(models.Model):
    title = models.CharField('Название', max_length=150)
    description = models.TextField('Описание')
    release_date = models.DateField('Дата премьеры')
    production_year = models.PositiveIntegerField('Год производства')
    rating = models.PositiveSmallIntegerField('Рейтинг фильма', choices=[(i, str(i)) for i in range(1, 11)])
    duration = models.PositiveIntegerField('Продолжительность (в минутах)')
    poster = models.ImageField('Постер', upload_to='poster_image/')
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
    movie_categories = models.ManyToManyField(
        'Category',
        blank=True,
        related_name='movies'
    )
    series_categories = models.ManyToManyField(
        'Category',
        blank=True,
        related_name='series'
    )
    genres = models.ManyToManyField(
        'Genre',
        blank=True
    )
    country = models.ManyToManyField(
        'Country',
        blank=True
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
    is_film = models.BooleanField(help_text='Отметьте, если это фильм, и снимите, если это сериал.')

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
    categories = models.ManyToManyField(
        'Category',
        related_name='series_categories',
        blank=True
    )
    # genres = models.ManyToManyField('Genre')
    # country = models.ManyToManyField('Country')
    # film_crews = models.ManyToManyField('FilmCrew', related_name='series')


    def __str__(self):
        return f"Серия {self.number}"

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'


class Category(models.Model):
    title = models.CharField(
        'Категория',
        max_length=100,

    )
    image = models.ImageField(upload_to='category_img/')

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
    genre_img = models.ImageField(upload_to='genre_img/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Country(models.Model):
    title = models.CharField(
        'Страна производства',
        max_length=150
    )
    country_img = models.ImageField(upload_to='country_img/')

    def __str__(self):
        return self.title

class FilmCrew(models.Model):
    name = models.CharField(
        'Имя',
        max_length=150
    )
    birth_date = models.DateField('Дата рождения')
    birthplace = models.CharField(
        'Место рождения',
        max_length=150
    )
    image = models.ImageField(
        upload_to='film_crew_img/',
        blank=True, null=True
    )
    position = models.CharField(
        'Роль в фильме',
        max_length=100
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    genres = models.ManyToManyField(
        Genre,
        blank=True,

    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Съемочная группа'
        verbose_name_plural = 'Съемочная группа'


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='favorited_by', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')



class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField('Оценка', choices=[(i, str(i)) for i in range(1, 11)])
    created_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )
    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return f"{self.movie.title} - {self.user.username}: {self.score}"







