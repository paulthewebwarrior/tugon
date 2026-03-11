from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import click
from flask.cli import with_appcontext

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Change to your Postgres URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

@click.command('create-tables')
@with_appcontext
def create_tables_command():
    db.create_all()
    click.echo('Tables created.')

app.cli.add_command(create_tables_command)

@app.route('/')
def index():
    return 'Hello, world!'

if __name__ == '__main__':
    app.run(debug=True)
