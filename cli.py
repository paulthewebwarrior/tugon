import click
from flask.cli import with_appcontext
from models_pg import db

def create_tables():
    db.create_all()

@click.command('create-tables')
@with_appcontext
def create_tables_command():
    """Create database tables."""
    create_tables()
    click.echo('Tables created.')
