import enum
import time
from typing import Dict, List, Union

import click
import requests

BASE_URL = "https://v2.jokeapi.dev/joke/Any"


class JokeType(enum.Enum):
    SINGLE = "single"
    TWO_PART = "twopart"


def get_joke_request() -> Union[List, Dict]:
    """
    Gets joke from API https://v2.jokeapi.dev/
    """
    try:
        response = requests.get(BASE_URL)
        return response.json()
    except (IOError, ValueError):
        return {"message": "Error getting joke from server"}


def show_progress_bar(message, delay_time=3):
    with click.progressbar(
        range(delay_time),
        label=message,
        show_eta=False,
        show_percent=False,
        fill_char="?",
    ) as progress_bar:
        for _ in progress_bar:
            time.sleep(1)


def get_joke() -> None:
    joke = get_joke_request()
    joke_type = joke.get("type")
    if joke_type == JokeType.SINGLE.value:
        formatted_joke = click.style(joke.get("joke"), fg="green", bold=True)
        click.echo(formatted_joke)
    elif joke_type == JokeType.TWO_PART.value:
        joke_setup = joke.get("setup")
        formatted_setup = click.style(joke_setup, fg="green", bold=True)
        click.echo(formatted_setup)
        show_progress_bar("Loading")
        joke_delivery = joke.get("delivery")
        formatted_delivery = click.style(
            joke_delivery, fg="green", bold=True, underline=True
        )
        click.echo(formatted_delivery)
    else:
        error = joke.get("message", "Error processing request")
        formatted_error = click.style(error, fg="red")
        click.echo(formatted_error)


@click.command(name="Joke of the Day CLI Application")
def jokes():
    """
    The "Joke of the Day" CLI application is a fun and lighthearted tool
    that fetches and displays a random joke for users to enjoy each day.
    """
    get_joke()


if __name__ == "__main__":
    jokes()
