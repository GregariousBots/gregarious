"""Run tasks that support easy linting without reliance on pre-commits."""
import inspect
import os

import tasks as module
from invoke import task
from rich.console import Console

console = Console()

BLACK = "black"
RUN_LINTER = "run_linter"
SPACE_SEPARATOR = " "
VIRTUAL_ENV_COMMAND = "echo $VIRTUAL_ENV"


def check_virtualenv_exists():
    """Determine if there is a virtual environment that contains the existing tools."""
    if os.getenv("VIRTUAL_ENV") is not None:
        return True
    return False


def extract_directories(search_directory="."):
    """Extract all of the top-level directories in the provided directory."""
    directory_list = []
    # iterate through all of the directories in the provided search_directory
    for filename in os.listdir(search_directory):
        # only proceed if the current file is a directory
        if os.path.isdir(os.path.join(search_directory, filename)):
            # only proceed if the directory is not a hidden directory
            # that starts with period (i.e., ".git" is a hidden directory)
            if not filename.startswith("."):
                directory_list.append(filename)
    # return the list of the non-hidden directories
    return directory_list


def extract_linter_functions():
    """Extract a list of all of the linter functions in this module."""
    functions = dict(inspect.getmembers(module, inspect.isfunction))
    linter_functions = []
    for function in functions:
        if RUN_LINTER in function:
            linter_functions.append(function)
    return linter_functions


def invoke_linter_command(c, linter_command):
    """Run the provided linter_command and return the result."""
    console.print()
    console.print(":zap:", "Running:", linter_command)
    c.run(linter_command)
    console.print()


def run_linter_black(c, check, directory_list):
    """Run the black linter to check and fix Python code formatting."""
    directories = SPACE_SEPARATOR.join(directory_list)
    black_command = SPACE_SEPARATOR.join([BLACK, check, directories])
    invoke_linter_command(c, black_command)


@task
def lint(c, check="--check"):
    """Run all of the linters installed inside of the virtualenv created by Poetry."""
    console.print(":rocket:  Running all linters ...")
    if check_virtualenv_exists():
        console.print()
        console.print("Running in a virtual environment:")
        c.run(VIRTUAL_ENV_COMMAND)
        console.print()
        linters = extract_linter_functions()
        console.print("Available linters functions:", SPACE_SEPARATOR.join(linters))
        print()
        directory_list = extract_directories(".")
        console.print("Directories subject to linting:", directory_list)
        linters = extract_linter_functions()
        for linter in linters:
            linter_to_call = getattr(module, linter)
            linter_to_call(c, check, directory_list)
    else:
        console.print("Not running in a virtual environment!")
    console.print("...", "Done running all linters", ":rocket:")
