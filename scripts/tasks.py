"""Run tasks that support easy linting without reliance on pre-commits."""
import os

from invoke import task
from rich.console import Console

console = Console()

BLACK = "black"
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


def run_linter_command(c, linter_command):
    """Run the provided linter_command and return the result."""
    console.print()
    console.print(":zap:", "Running:", linter_command)
    c.run(linter_command)
    console.print()


def run_black_linter(c, check, directory_list):
    """Run the black linter to check and fix Python code formatting."""
    space_separator = " "
    directories = space_separator.join(directory_list)
    print(directories)
    black_command = space_separator.join([BLACK, check, directories])
    run_linter_command(c, black_command)


@task
def lint(c, check="--check"):
    """Run all of the linters installed inside of the virtualenv created by Poetry."""
    console.print(":rocket:  Running all linters ...")
    if check_virtualenv_exists():
        console.print()
        console.print("Running in a virtual environment:")
        c.run(VIRTUAL_ENV_COMMAND)
        console.print()
        directory_list = extract_directories(".")
        print(directory_list)
        run_black_linter(c, check, directory_list)
    else:
        console.print("Not running in a virtual environment!")
    console.print("...", "Done running all linters", ":rocket:")
