from __future__ import annotations

import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
from random import randint
from typing import List, Optional, Sequence, Sized, TYPE_CHECKING, TextIO

import click
from flask.cli import FlaskGroup
from loguru import logger

from project import app, db, user_manager
from project.database.accommodation import Accommodation, Room
from project.database.booking import Booking
from project.database.party import Guest, Party
from project.database.users import Role, User, UserRoles
from project.guest.token import get_token

if TYPE_CHECKING:
    from PIL import Image as PILImage


cli = FlaskGroup(app)


def batch(iterable, n=1):
    n_items = len(iterable)
    for index in range(0, n_items, n):
        yield iterable[index : min(index + n, n_items)]


def generate_qr_code_pil_image(guest_code: str) -> PILImage:
    import qrcode

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, border=3, box_size=14)
    qr.add_data(f"https://snapewedding.com{user_manager.USER_REGISTER_URL}?guest_code={guest_code}")
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    assert image.size == (602, 602)
    return image


def one_inch_qr_codes_to_printable_pdf(
    qr_code_images: Sized[PILImage],
    out_dir: Path,
    width: float = 8.3,
    height: float = 11.7,
    x_margin: float = 0.6732283,
    y_margin: float = 0.405512,
    x_spacing: float = 0.2,
    y_spacing: float = 0,
    max_n_rows: int = 11,
    max_n_cols: int = 6,
    dpi: float = 600,
) -> None:
    """
    This is a helper method to generate a printable PDF that prints nicely using the paper I bought (Herma 10107).
    Note that the default values come from the herma website but required some fudging to actually print with
    my printer:

        x_margin = 0.346457 + 0.11811 / 2.0 = 0.405512
        y_margin = 0.6338583 + 0.11811 / 3.0 = 0.6732283

    All the values are in inches in everything currently assumes the incoming QR code images are in the correct
    number of pixels for a one inch QR code at 600 DPI (e.g. approximately 600x600).

    Args:
        qr_code_images: List of PIL images to create PDFs from
        out_dir: Output directory to save PDF to
        width: Width of the output page
        height: Height of the output page
        x_margin: Horizontal margin e.g. how far away from left edge to start pasting
        y_margin: Vertical margin e.g. how far away from top edge to start pasting
        x_spacing: Spacing between QR codes horizontally across the page
        y_spacing: Spacing between QR codes vertically down the page
        max_n_rows: Maximum number of rows down the page
        max_n_cols: Maximum number of QR codes per row
        dpi: DPI to generate printed page at
    """
    from PIL import Image as PILImage

    assert dpi == 600, "Only DPI of 600 is supported"
    width = int(width * dpi)
    height = int(height * dpi)
    x_margin = int(x_margin * dpi)
    y_margin = int(y_margin * dpi)
    x_spacing = int(x_spacing * dpi)
    y_spacing = int(y_spacing * dpi)

    qr_code_size = int(dpi)

    row_index = 0
    page_index = 0
    page = PILImage.new("RGB", (width, height), "white")
    for qr_code_row in batch(qr_code_images, n=max_n_cols):
        y = y_margin + row_index * qr_code_size + row_index * y_spacing
        for col_index, qr_code in enumerate(qr_code_row):
            x = x_margin + col_index * qr_code_size + col_index * x_spacing
            page.paste(qr_code, box=(x, y))
        row_index += 1

        if row_index == max_n_rows:
            page.save(str(out_dir / f"page_{page_index}.pdf"), resolution=dpi)
            page = PILImage.new("RGB", (width, height), "white")
            row_index = 0
            page_index += 1

    # Make sure we save the final page no matter what
    page.save(str(out_dir / f"page_{page_index}.pdf"), resolution=dpi)


def _add_admin_user() -> None:
    role = Role(name="admin")
    db.session.add(role)
    db.session.flush()

    password = os.getenv("ADMIN_USER_PASSWORD") or "password"
    user = User(
        email="admin@snapewedding.com",
        email_confirmed_at=datetime.utcnow(),
        password=user_manager.hash_password(password),
    )
    db.session.add(user)
    db.session.flush()

    user_role = UserRoles(user_id=user.id, role_id=role.id)
    db.session.add(user_role)


def _add_accommodation(n_rooms: int = 2) -> List[Room]:
    assert n_rooms > 0
    from faker import Faker

    fake = Faker()

    lat, long = fake.local_latlng(country_code="DE", coords_only=True)
    accommodation = Accommodation(
        name=fake.city(),
        website=fake.domain_name(),
        latitude=lat,
        longitude=long,
        address=fake.address().replace("\n", ", "),
        description=fake.paragraph(),
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


def _add_party(n_guests: int = 2, create_user: bool = False, add_booking_to_room: Optional[Room] = None) -> None:
    assert n_guests > 0
    from faker import Faker

    fake = Faker()
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
            check_in=fake.date_between_dates(app.config["BOOKING_MIN_DATE"], app.config["WEDDING_DATETIME"].date()),
            check_out=fake.date_between_dates(
                app.config["WEDDING_DATETIME"].date() + timedelta(days=1), app.config["BOOKING_MAX_DATE"]
            ),
        )
        logger.info(f"{booking}")
        db.session.add(booking)


@cli.command("create_db")
def create_db() -> None:
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

    # Create admin user
    _add_admin_user()

    db.session.commit()


@cli.command("seed_from_csv")
@click.argument("csv_file_path", type=Path)
def seed_from_csv(csv_file_path: Path) -> None:
    with csv_file_path.open("rt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        for (party_id, guests, room_id, check_in, check_out) in csv_reader:
            guests = guests.split("&")

            party = Party(id=int(party_id), guest_code=get_token())
            db.session.add(party)
            db.session.flush()
            logger.info(f"{party}")

            for guest in guests:
                first_name, last_name = guest.split(",")
                guest = Guest(party_id=party.id, first_name=first_name.strip(), last_name=last_name.strip())
                logger.info(f"  {guest}")
                db.session.add(guest)

            if room_id != "-1":
                check_in_date = datetime.strptime(check_in, "%d.%m.%Y")
                check_out_date = datetime.strptime(check_out, "%d.%m.%Y")
                booking = Booking(
                    party_id=party.id, room_id=int(room_id), check_in=check_in_date, check_out=check_out_date,
                )
                logger.info(f"    {booking}")
                db.session.add(booking)

    logger.info("Adding admin user")
    _add_admin_user()

    db.session.commit()


@cli.command("generate_qr_codes")
@click.option("--party-ids-file", type=click.File("rt"))
def generate_qr_codes(party_ids_file: Optional[TextIO]) -> None:
    if party_ids_file is not None:
        party_ids = [int(pid.strip()) for pid in party_ids_file.readlines()]
        all_parties = db.session.query(Party).filter(Party.id.in_(party_ids)).order_by(Party.id).all()
    else:
        all_parties = db.session.query(Party).order_by(Party.id).all()

    out_dir = Path("qr_codes")
    out_dir.mkdir(exist_ok=True)

    qr_code_images = []
    for party in all_parties:
        guest_names = ", ".join(g.full_name for g in party.guests)
        logger.info(f"Generating QR code for party {party.id} with guests: {guest_names}")

        guest_code = party.guest_code
        image = generate_qr_code_pil_image(guest_code)
        image.save(str(out_dir / f"{party.id:02d}.png"))
        qr_code_images.append(image)

    one_inch_qr_codes_to_printable_pdf(qr_code_images, out_dir)


if __name__ == "__main__":
    cli()
