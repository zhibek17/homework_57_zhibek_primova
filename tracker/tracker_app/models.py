from django.db import models
from django.core.validators import MinLengthValidator


class AbstractModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Время изменения', auto_now=True)

    class Meta:
        abstract = True


class Type(AbstractModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Status(AbstractModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Task(AbstractModel):
    TYPE_CHOICES = (
        ('Task', 'Задача'),
        ('Bug', 'Ошибка'),
        ('Enhancement', 'Улучшение')
    )

    STATUS_CHOICES = (
        ('New', 'Новый'),
        ('In Progress', 'В процессе'),
        ('Done', 'Выполнено')
    )

    summary = models.CharField(max_length=100, verbose_name='Краткое описание')
    description = models.TextField(blank=True, null=True, verbose_name='Полное описание', validators=[
        MinLengthValidator(5, message='Минимальная длина описания - 5 символов')])
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ManyToManyField(Type, verbose_name='Тип')

    def __str__(self):
        return self.summary
