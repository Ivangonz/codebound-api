from invoke.tasks import Task
from invoke.context import Context

@Task
def run(c: Context):
    """Run the FastAPI server with uvicorn"""
    c.run("uvicorn app.main:app --reload --port 8000")

@Task
def lint(c: Context):
    """Run Ruff and Pyright"""
    c.run("ruff check app")
    c.run("pyright")

@Task
def test(c: Context):
    """Run pytest"""
    c.run("pytest -q")
