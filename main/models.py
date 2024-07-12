from django.db import models

class Size(models.Model):
    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(models.Model):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['tittle']
    sizes = models.ManyToManyField(Size, blank=True)
    tittle = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Модель")
    price = models.FloatField(verbose_name="Цена")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    def __str__(self):
        return self.tittle

class Review(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    text = models.TextField()
    stars = models.IntegerField(
        choices=(
            (1, '*'),
            (2, '* *'),
            (3, '* * *'),
            (4, '* * * *'),
            (5, '* * * * *'),
        )
    )
    author = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.author
