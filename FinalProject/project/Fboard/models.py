from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    title = models.CharField(max_length=200)
    content = RichTextUploadingField(verbose_name='Объявление')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])


class Author(models.Model):
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    name = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')
    is_subscriber = models.BooleanField(verbose_name='Подписчик', default=False)
    email = models.EmailField()
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name.username}'


class Category(models.Model):
    categories = [('tank', 'Танки'),
                  ('healers', 'Хилы'),
                  ('dd', 'ДД'),
                  ('traders', 'Торговцы'),
                  ('guildmasters', 'Гилдмастеры'),
                  ('questgivers', 'Квестгиверы'),
                  ('blacksmiths', 'Кузнецы'),
                  ('leatherworkers', 'Кожевники'),
                  ('potionmasters', 'Зельевары'),
                  ('spellmasters', 'Мастера заклинаний'),
                  ]
    name = models.CharField(max_length=100, choices=categories, default='tank', unique=True)

    def __str__(self):
        return self.name


class Reply(models.Model):
    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name='Автор')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Объявление')
    content = models.TextField(verbose_name='Отклик')
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.content[0:32]}'


class Media(models.Model):
    file = models.FileField(upload_to='media/')
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name






