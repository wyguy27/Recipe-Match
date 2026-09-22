from django.db import models


class Diet(models.Model):
    name = models.CharField(max_length=50)


class Intolerances(models.Model):
    name = models.CharField(max_length=50)


class Equipment(models.Model):
    spoon_id = models.IntegerField()
    name = models.CharField(max_length=100)


class Type(models.Model):
    name = models.CharField(max_length=50)


class Ingredient(models.Model):
    spoon_id = models.IntegerField()
    name = models.CharField(max_length=200)


class Recipe(models.Model):
    spoon_id = models.IntegerField()
    name = models.CharField(max_length=200)
    cuisine = models.CharField(max_length=50)
    ingredients = models.ManyToManyField(RecipeIngredient)
    instructions = models.CharField(max_length=4000)
    image = models.CharField(max_length=200)
    prep_time = models.IntegerField()
    servings = models.IntegerField()
    calories = models.IntegerField()
    diet = models.ManyToManyField(Diet)
    intolerances = models.ManyToManyField(Intolerances)
    equipment = models.ManyToManyField(Equipment)
    type = models.ManyToManyField(Type)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField()
    unit = models.CharField(max_length=100)