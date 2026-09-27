"""
Fills the local SQLite database with 99 information from 99 recipes (daily limit)
Ensure you have a ".env" file with an API_KEY variable in your project's root directory
"""

import json
import requests
import dotenv


def call(query: str) -> None:
    """Queries Spoonacular API for recipe information"""
    pass
    

def save_db() -> None:
    """Saves API response to local database"""
    pass


def main() -> None:
    ENV = dotenv.load_dotenv("./.env")
    query: str = ""


if __name__ == "__main__":
    main()