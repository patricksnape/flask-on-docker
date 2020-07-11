from datetime import datetime

from flask.cli import FlaskGroup

from project import app, db, user_manager
from project.database.party import Party, Guest
from project.database.users import User

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db() -> None:
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db() -> None:
    party = Party(guest_code="ABCD12")
    db.session.add(party)
    db.session.flush()

    user = User(
        email="paul@test.com",
        email_confirmed_at=datetime.utcnow(),
        password=user_manager.hash_password("password"),
        party_id=party.id,
    )
    db.session.add(user)

    guest1 = Guest(party_id=party.id, first_name="Paul", last_name="Smith")
    db.session.add(guest1)
    guest2 = Guest(party_id=party.id, first_name="Jan", last_name="Smith")
    db.session.add(guest2)

    db.session.commit()


if __name__ == "__main__":
    cli()
