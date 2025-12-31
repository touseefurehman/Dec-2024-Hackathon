from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Define category choices for home page links
CATEGORY_CHOICES = (
    ('Starter', 'Starter'),
    ('Main', 'Main'),
    ('Side', 'Side'),
    ('Dessert', 'Dessert'),
)


# Create your models here.
STATUS = ((0, "Draft"), (1, "Published"))


class Recipe(models.Model):
    """ Model for recipes """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=100, unique=True)
    cooking_time = models.IntegerField(
        help_text="Cooking time in minutes",
        default=30)
    ingredients = models.TextField()
    instructions = models.TextField()
    image = CloudinaryField('image', default='https://res.cloudinary.com/dn7apsma3/image/upload/v1234567890/placeholder.png')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    favourites = models.ManyToManyField(
        User,
        related_name='favourite_recipes',
        blank=True)
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='Main'
    )
    recommended = models.BooleanField(default=False)
    servings = models.IntegerField(
        help_text="Number of servings",
        default=4)

    def get_ingredients_list(self):
        """
        Return ingredients as a list,
        separated each ingredient by newline
        """
        return [
            ing.strip() for ing in self.ingredients.split('\n') if ing.strip()  # noqa
        ]

    def get_instructions_list(self):
        """
        Returns instructions as a list ,
        splitting by 'step' markers
        """
        steps = [
            step.strip() for step in self.instructions.split('step') if step.strip()  # noqa
        ]
        return [step.split('.', 1)[-1].strip() for step in steps]

    class Meta:
        """
        Orders recipies by:
        1. Recipes in draft.
        2. Oldest updated.
        i.e. shows oldest draft recipies which have not be published first.
        """
        ordering = ["status", "-updated_on"]

    def __str__(self):
        """Displays most useful recipe information."""
        return f"{self.status} | {self.author} | {self.title} | {self.description}"  # noqa
