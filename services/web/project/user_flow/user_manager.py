from __future__ import annotations

from typing import Optional
from urllib.parse import quote

from flask import request, redirect, url_for, current_app, render_template, flash
from flask_login import current_user
from flask_user import UserManager, signals
from flask_user.translation_utils import lazy_gettext as _
from wtforms import ValidationError

from project.database.users import User
from project.database.party import Party
from project.user_flow.forms import GuestCodeRegisterForm


class GuestCodeUserExists(ValueError):
    pass


class WeddingUserManager(UserManager):
    def customize(self, app):

        # Configure customized forms
        self.RegisterFormClass = GuestCodeRegisterForm

    @staticmethod
    def password_validator(form, field):
        password = list(field.data)
        if len(password) < 6:
            raise ValidationError(_("Password must have at least 6 characters"))

    def verify_guest_code_not_registered(self, guest_code: Optional[str]) -> None:
        if guest_code is not None and User.get_by_guest_code(guest_code, self.db.session) is not None:
            raise GuestCodeUserExists()

    def user_is_authenticated(self):
        return self.call_or_get(current_user.is_authenticated) and self.db_manager.user_has_confirmed_email(
            current_user
        )

    def forgot_password_view(self):
        if self.user_is_authenticated():
            return redirect(self.USER_AFTER_LOGIN_ENDPOINT)
        else:
            return super().forgot_password_view()

    def register_view(self):
        # We have to customize the registration flow because of our requirement
        # for the guest code to exist - but this means we basically disable
        # some of the existing flows in Flask-User - so we just assert that
        # those values respect the flow we actually take here
        assert not self.USER_REQUIRE_INVITATION

        if self.user_is_authenticated():
            return redirect(self.USER_AFTER_LOGIN_ENDPOINT)

        try:
            return self._registration_flow()
        except GuestCodeUserExists:
            flash(
                "The provided Guest Code has already been claimed. Please login using your email and password.",
                "error",
            )
            return redirect(url_for("user.login"))

    def _registration_flow(self):
        safe_next_url = self._get_safe_next_url("next", self.USER_AFTER_LOGIN_ENDPOINT)
        safe_reg_next_url = self._get_safe_next_url("reg_next", self.USER_AFTER_REGISTER_ENDPOINT)

        # Initialize form
        login_form = self.LoginFormClass()  # for login_or_register.html
        register_form = self.RegisterFormClass(request.form)  # for register.html

        if request.method != "POST":
            login_form.next.data = register_form.next.data = safe_next_url
            login_form.reg_next.data = register_form.reg_next.data = safe_reg_next_url

        # Process valid POST
        if register_form.validate_on_submit():
            self.verify_guest_code_not_registered(register_form.guest_code.data)

            user = self.db_manager.add_user()
            register_form.populate_obj(user)
            user_email = self.db_manager.add_user_email(user=user, is_primary=True)
            register_form.populate_obj(user_email)

            # Store password hash instead of password
            user.password = self.hash_password(user.password)

            self.db_manager.save_user_and_user_email(user, user_email)
            self.db_manager.commit()

            if self.USER_SEND_REGISTERED_EMAIL:
                try:
                    # Send 'confirm email' or 'registered' email
                    self._send_registered_email(user, user_email, self.USER_ENABLE_CONFIRM_EMAIL)
                except Exception as e:
                    self.db_manager.delete_object(user)
                    self.db_manager.commit()
                    raise

            signals.user_registered.send(current_app._get_current_object(), user=user)

            if self.USER_ENABLE_CONFIRM_EMAIL:
                safe_reg_next_url = self.make_safe_url(register_form.reg_next.data)
                return redirect(safe_reg_next_url)

            if "reg_next" in request.args:
                safe_reg_next_url = self.make_safe_url(register_form.reg_next.data)
            else:
                safe_reg_next_url = self._endpoint_url(self.USER_AFTER_CONFIRM_ENDPOINT)

            if self.USER_AUTO_LOGIN_AFTER_REGISTER:
                return self._do_login_user(user, safe_reg_next_url)
            else:
                return redirect(url_for("user.login") + "?next=" + quote(safe_reg_next_url))

        guest_code = request.args.get("guest_code")
        guests = None
        if guest_code is not None:
            self.verify_guest_code_not_registered(guest_code)
            party = Party.get_by_guest_code(guest_code, self.db.session)
            if party is not None:
                guests = party.guests

        self.prepare_domain_translations()
        return render_template(
            self.USER_REGISTER_TEMPLATE,
            form=register_form,
            login_form=login_form,
            register_form=register_form,
            guests=guests,
        )
