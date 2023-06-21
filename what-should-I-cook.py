#!/usr/bin/env python3

import click
import os
import subprocess

# use the RECIPES_HOME environment variable if it exists, otherwise assume the current working directory is fine
RECIPES_HOME = os.getenv('RECIPES_HOME', os.getcwd())


@click.command()
def what_should_i_cook():
    # Ask the user for ingredients
    ingredients = click.prompt("Aw, spud, let me help you out. What ingredients do you have? (separated by commas)")

    # Split the user input into individual ingredients
    ingredient_list = [ingredient.strip() for ingredient in ingredients.split(",")]

    # Execute the recipemd-find command with the provided ingredients
    command = f"recipemd-find -e \"{generate_search_query(ingredient_list)}\" -1 recipes"
    output = subprocess.check_output(command, shell=True, cwd=RECIPES_HOME).decode("utf-8")

    # Parse the output to extract the recipe choices
    recipes = parse_recipes(output)

    # Prompt the user to select a recipe
    click.echo("Choose a recipe from the options below:")
    for i, recipe in enumerate(recipes, start=1):
        click.echo(f"{i}. {recipe}")

    # Ask the user to pick a recipe
    selection = int(click.prompt("Enter the number of the recipe you want to view"))

    # Show the selected recipe
    if 1 <= selection <= len(recipes):
        show_recipe(recipes[selection - 1])
    else:
        click.echo("Invalid selection. Exiting...")


def generate_search_query(ingredients):
    # Generate the search query for the recipemd-find command
    query_parts = [f"ingr:{ingredient}" for ingredient in ingredients]
    return " or ".join(query_parts)


def parse_recipes(output):
    # Parse the output of the recipemd-find command to extract the recipe choices
    return output.strip().split("\n")


def show_recipe(recipe):

    # Clear the screen
    clear_screen()

    # Execute a command to display the details of the selected recipe
    command = f"rich {recipe}"
    subprocess.run(command, shell=True, cwd=RECIPES_HOME)

    # skip a line, it looks better that way
    print()

# Function to clear the screen based on the operating system
def clear_screen():
    if os.name == 'posix':  # Unix/Linux/MacOS
        subprocess.call('clear', shell=True)
    elif os.name == 'nt':  # Windows
        subprocess.call('cls', shell=True)

if __name__ == "__main__":
    what_should_i_cook()

