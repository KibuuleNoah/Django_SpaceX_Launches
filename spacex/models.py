from django.db import models

# Create your models here.


class Launch(models.Model):
    name = models.CharField(max_length=50)
    image = models.URLField(null=True)
    details = models.TextField(null=True)
    article_link = models.URLField(null=True)
    reddit_link = models.URLField(null=True)
    wikipedia_link = models.URLField(null=True)
    status = models.CharField(
        max_length=1,
        choices={
            "S": "Success",
            "U": "Upcoming",
            "F": "Failed",
        },
    )
    date = models.DateField()
