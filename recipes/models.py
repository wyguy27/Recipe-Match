from django.db import models


class Recipe(models.Model):
    spoonacular_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=256)
    image = models.URLField(blank=True)
    ready_time = models.PositiveIntegerField(null=True)
    servings = models.PositiveIntegerField(null=True)
    instructions = models.TextField()
    calories = models.DecimalField(null=True)
    cuisines = models.ManyToManyField(
        "Cuisine",
        related_name="recipes",
        blank=True,
        null=True,
    )
    diets = models.ManyToManyField(
        "Diet",
        related_name="recipes",
        blank=True,
        null=True,
    )
    intolerances = models.ManyToManyField(
        "Intolerance",
        related_name="recipes",
        blank=True,
        null=True,
    )
    equipment = models.ManyToManyField(
        "Equipment",
        related_name="recipes",
        blank=True,
        null=True,
    )
    types = models.ManyToManyField(
        "RecipeType",
        related_name="recipes",
        blank=True,
        null=True,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    spoonacular_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=256)
    image = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
    )
    amount = models.DecimalField(null=True)
    unit = models.CharField(max_length=50, blank=True)
    text_measurement = models.TextField(blank=True) # Example: "1 tbsp sugar"

    # Required for unique recipe / ingredient pairs in DB
    class Meta:
        unique_together = ("recipe", "ingredient")


class Cuisine(models.Model):
    name = models.CharField(max_length = 50, unique=True)

    def __str__(self) -> str:
        return self.name


class Diet(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Intolerance(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Equipment(models.Model):
    spoonacular_id = models.PositiveIntegerField(null=True, unique=True)
    name = models.CharField(max_length=100)
    image = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.name


class RecipeType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name