from arkitekt import register
import time


@register
def create_n_string(n: int = 10, timeout: int = 2) -> str:
    """Append World to String

    Appends world to string

    Args:
        hello (str): The first part of the string
    """
    for i in range(n):
        print(i)
        time.sleep(timeout)
        return f"Hello {i}"


@register
def append_world(hello: str) -> str:
    """Append World to String

    Appends world to string

    Args:
        hello (str): The first part of the string
    """
    return hello + " World"


@register
def print_string(input: str) -> None:
    """By World

    Prints hello world to the console

    Args:
        hello (str): The hello world string
    """
    print(input)
