from datetime import datetime, timedelta
from random import randint
from typing import Optional, List

from faker import Faker
from flask.cli import FlaskGroup

from project import app, db, user_manager
from project.database.accommodation import Accommodation, Room
from project.database.booking import Booking
from project.database.party import Party, Guest
from project.database.users import User
from project.token.token import get_token
from loguru import logger

fake = Faker()
cli = FlaskGroup(app)


def _add_accommodation(n_rooms: int = 2) -> List[Room]:
    assert n_rooms > 0

    lat, long = fake.local_latlng(country_code="DE", coords_only=True)
    accommodation = Accommodation(
        name=fake.city(),
        website=fake.domain_name(),
        latitude=lat,
        longitude=long,
        address=fake.address().replace("\n", ", "),
    )
    logger.info(f"{accommodation}")
    db.session.add(accommodation)
    db.session.flush()

    rooms = []
    for _ in range(n_rooms):
        room = Room(accommodation_id=accommodation.id, name=fake.city(), price_per_night=randint(50, 200))
        rooms.append(room)
        logger.info(f"{room}")
    db.session.add_all(rooms)

    return rooms


def _add_party(n_guests: int = 2, create_user: bool = False, add_booking_to_room: Optional[Room] = None):
    assert n_guests > 0

    party = Party(guest_code=get_token())
    logger.info(f"{party}")
    db.session.add(party)
    db.session.flush()

    guests = []
    for _ in range(n_guests):
        guest = Guest(party_id=party.id, first_name=fake.first_name(), last_name=fake.last_name())
        guests.append(guest)
        logger.info(f"{guest}")
    db.session.add_all(guests)

    if create_user:
        first_guest = guests[0]
        user = User(
            email=f"{first_guest.first_name}@test.com",
            email_confirmed_at=datetime.utcnow(),
            password=user_manager.hash_password("password"),
            party_id=party.id,
        )
        logger.info(f"{user}")
        db.session.add(user)

    if add_booking_to_room is not None:
        booking = Booking(
            party_id=party.id,
            room_id=add_booking_to_room.id,
            check_in=fake.date_between_dates(app.config["BOOKING_MIN_DATE"], app.config["WEDDING_DATE"]),
            check_out=fake.date_between_dates(app.config["WEDDING_DATE"], app.config["BOOKING_MAX_DATE"]),
        )
        logger.info(f"{booking}")
        db.session.add(booking)


@cli.command("create_db")
def create_db() -> None:
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db() -> None:
    rooms = _add_accommodation(n_rooms=2)

    # Registered Party with booking
    logger.info("**** Registered Party with booking ****")
    _add_party(n_guests=2, create_user=True, add_booking_to_room=rooms[0])

    # Unregistered Party with booking\
    logger.info("**** Unregistered Party with booking ****")
    _add_party(n_guests=2, create_user=False, add_booking_to_room=rooms[1])

    # Registered Party without booking
    logger.info("**** Registered Party without booking ****")
    _add_party(n_guests=3, create_user=True)

    db.session.commit()


if __name__ == "__main__":
    cli()
