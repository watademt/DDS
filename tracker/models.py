from django.db import models
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название статуса")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название типа")

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название категории")
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Тип операции"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['type__name', 'name']
        # Уникальность связки "имя + тип", чтобы не создать две одинаковые категории в одном типе
        unique_together = ('name', 'type')

    def __str__(self):
        return f"{self.name} ({self.type.name})"


class Subcategory(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название подкатегории")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['category__name', 'name']
        unique_together = ('name', 'category')

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Transaction(models.Model):
    # Используем default=timezone.now, а не auto_now_add=True,
    # чтобы поле заполнялось автоматически, но оставалось доступным для ручного редактирования.
    date = models.DateField(default=timezone.now, verbose_name="Дата")

    # Используем PROTECT для финансовой истории. Удалить справочник можно будет
    # только если на него не ссылается ни одна транзакция.
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="Статус"
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="Тип"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="Категория"
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="Подкатегория"
    )

    # max_digits=12 (до миллиардов), decimal_places=2 (копейки)
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")

    # Для текстовых необязательных полей в Django используется blank=True без null=True
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        # Сортировка по умолчанию: сначала свежие записи
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.date.strftime('%d.%m.%Y')} | {self.type.name}: {self.amount} руб. ({self.category.name})"