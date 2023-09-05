from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

LIMIT_TEXT = 20


class Group(models.Model):
    title = models.CharField('Название группы', max_length=200)
    slug = models.SlugField('Номер группы', unique=True, max_length=50)
    description = models.TextField('Описание группы', max_length=200)

    def __str__(self):
        return self.title[:LIMIT_TEXT]


class Post(models.Model):
    text = models.TextField('Текст статьи')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='группа статей'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name='картинка статьи'
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:LIMIT_TEXT]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Имя автора'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Имя поста'
    )
    text = models.TextField(
        max_length=300,
        verbose_name='Текст комментария'
    )
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return f'{self.author} оставил комментарий {self.text}'[:LIMIT_TEXT]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Укажите подписчика'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='На кого подписываемся'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.following}'[:LIMIT_TEXT]
