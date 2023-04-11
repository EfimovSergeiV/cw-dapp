from django.core.management.base import BaseCommand, CommandError
from catalog.models import ProductModel, CategoryModel
from pathlib import Path
from time import sleep


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


"""
class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ["headline"]

    def __str__(self):
        return self.headline

p1 = Publication(title="The Python Journal")
p1.save()
p2 = Publication(title="Science News")
p2.save()
p3 = Publication(title="Science Weekly")
p3.save()

a1 = Article(headline="Django lets you build web apps easily")
a1.save()

a1.publications.add(p1)

Publication.objects.filter(title__startswith="Science").delete()

===================================
print(product.related.all())
"""

cats_qs = CategoryModel.objects.all()
products_qs = ProductModel.objects.all()

product = products_qs.get(id=1880)
print(product.related.all())

cat = cats_qs.get(id=33)
print(cat.related_ct.all())


for cat in cats_qs:
    print(cat.name)