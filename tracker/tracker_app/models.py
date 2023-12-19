from django.db import models


class AbstractModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    class Meta:
        abstract = True


class Type(AbstractModel):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Status(AbstractModel):
    name = models.CharField(max_length=100, blank=False, null=False)

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

    summary = models.CharField(max_length=100, blank=False, null=False, verbose_name='Краткое описание')
    description = models.TextField(blank=True, null=True, verbose_name='Полное описание')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ManyToManyField(Type, verbose_name='Тип')

    def __str__(self):
        return self.summary