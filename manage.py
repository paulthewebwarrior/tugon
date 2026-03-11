from flask.cli import with_appcontext
from models_pg import db

import click

def create_tables():
    db.create_all()

@click.command(name='create_tables')
@with_appcontext
def create_tables_command():
    """Create database tables."""
    create_tables()
    click.echo('Tables created.')
