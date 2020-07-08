from datetime import datetime

from flask.cli import FlaskGroup

from project import app, db, User, user_manager

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    user = User(
        email='member@example.com',
        email_confirmed_at=datetime.utcnow(),
        password=user_manager.hash_password('password'),
    )
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    cli()
