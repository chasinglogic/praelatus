"""Execute hooks on a transition."""

from praelatus.tasks.app import app

@app.task
def fire_hooks(hooks, ticket):
