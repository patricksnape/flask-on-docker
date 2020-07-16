from datetime import datetime, timedelta

from flask.cli import FlaskGroup

from project import app, db, user_manager
from project.database.accomodation import Accommodation, Room
from project.database.booking import Booking
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
    accommodation = Accommodation(
        name="Empire State Building", website="google.com", google_maps_place_id="ChIJaXQRs6lZwokRY6EFpJnhNNE"
    )
    db.session.add(accommodation)
    db.session.flush()

    room_1 = Room(accomodation_id=accommodation.id, name="Penthouse", price_per_night=75)
    db.session.add(room_1)
    db.session.flush()

    room_2 = Room(accomodation_id=accommodation.id, price_per_night=23)
    db.session.add(room_2)
    db.session.flush()

    registered_party = Party(guest_code="ABCD12")
    db.session.add(registered_party)
    db.session.flush()

    registered_guest_1 = Guest(party_id=registered_party.id, first_name="Paul", last_name="Smith")
    registered_guest_2 = Guest(party_id=registered_party.id, first_name="Jan", last_name="Smith")

    user = User(
        email="paul@test.com",
        email_confirmed_at=datetime.utcnow(),
        password=user_manager.hash_password("password"),
        party_id=registered_party.id,
    )

    registered_booking = Booking(
        party_id=registered_party.id,
        room_id=room_1.id,
        check_in=app.config["WEDDING_DATE"] - timedelta(days=3),
        check_out=app.config["WEDDING_DATE"] + timedelta(days=2),
    )

    unregistered_party = Party(guest_code="123456")
    db.session.add(unregistered_party)
    db.session.flush()

    unregistered_guest_1 = Guest(party_id=unregistered_party.id, first_name="Tom", last_name="Jones")
    unregistered_guest_2 = Guest(party_id=unregistered_party.id, first_name="Tina", last_name="Jones")

    unregistered_booking = Booking(
        party_id=unregistered_party.id,
        room_id=room_2.id,
        check_in=app.config["WEDDING_DATE"] - timedelta(days=1),
        check_out=app.config["WEDDING_DATE"] + timedelta(days=4),
    )

    db.session.add_all(
        [
            registered_guest_1,
            registered_guest_2,
            user,
            registered_booking,
            unregistered_guest_1,
            unregistered_guest_2,
            unregistered_booking,
        ]
    )
    db.session.commit()


if __name__ == "__main__":
    cli()
