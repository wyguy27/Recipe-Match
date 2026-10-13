"""Tests how we can add tuples to our DB"""

import os, sys, django

# Sorry for the jank
DJANGO_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), r"recipes")
sys.path.insert(0, DJANGO_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from recipes.models import Diet

if __name__ == "__main__":
    payload = [
        "gluten free",
        "ketogenic",
        "vegetarian",
        "lacto-vegetarian",
        "ovo-vegetarian",
        "vegan",
        "pescetarian",
        "paleo",
        "primal",
        "low fodmap",
        "whole30",
        "dairy free",
    ]

    for diet in payload:
        Diet.objects.update_or_create(
            name=diet
        )

    print("Completed.")