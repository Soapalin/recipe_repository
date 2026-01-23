#!/usr/bin/env python3

from schema.db import SessionLocal, engine, Base
from schema.recipe import Recipe

def add_test_recipes():
    session = SessionLocal()
    try:
        # Create test recipes using SVGs
        recipes_data = [
            {
                "title": "Roasted Vegetable Orzo",
                "url": "https://example.com/roasted-vegetable-orzo",
                "author": "Placeholder Author 1",
                "img_path": "/images/roasted-vegetable-orzo.svg",
                "description": "Placeholder description for roasted vegetable orzo recipe.",
                "time_taken": 30,
                "servings": 4,
                "ingredients": "Placeholder ingredients: vegetables, orzo, herbs.",
                "instructions": "Placeholder instructions: Roast vegetables, cook orzo, mix together."
            },
            {
                "title": "Lemon Herb Chicken",
                "url": "https://example.com/lemon-herb-chicken",
                "author": "Placeholder Author 2",
                "img_path": "/images/lemon-herb-chicken.svg",
                "description": "Placeholder description for lemon herb chicken recipe.",
                "time_taken": 45,
                "servings": 4,
                "ingredients": "Placeholder ingredients: chicken, lemon, herbs.",
                "instructions": "Placeholder instructions: Marinate chicken, bake with lemon and herbs."
            },
            {
                "title": "Ginger Lime Salmon",
                "url": "https://example.com/ginger-lime-salmon",
                "author": "Placeholder Author 3",
                "img_path": "/images/ginger-lime-salmon.svg",
                "description": "Placeholder description for ginger lime salmon recipe.",
                "time_taken": 25,
                "servings": 2,
                "ingredients": "Placeholder ingredients: salmon, ginger, lime.",
                "instructions": "Placeholder instructions: Season salmon, bake with ginger and lime."
            }
        ]

        for data in recipes_data:
            recipe = Recipe(**data)
            session.add(recipe)

        session.commit()
        print("Added 3 test recipes successfully.")

    except Exception as e:
        session.rollback()
        print(f"Error adding recipes: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    add_test_recipes()