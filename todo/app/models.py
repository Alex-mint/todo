from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):

    name = models.CharField('Categoria', max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                verbose_name='Usuario',
                                on_delete=models.CASCADE, 
                                null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name='Categoria',
                                 null=True, blank=True,
                                 on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['completed', '-date']
