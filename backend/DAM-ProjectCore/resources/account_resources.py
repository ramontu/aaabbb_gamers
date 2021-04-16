#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64

import logging
import os
import random
import smtplib
import string

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import falcon
from falcon.media.validators import jsonschema
from sqlalchemy.orm.exc import NoResultFound

import messages
import settings
from db.models import User, UserToken, GenereEnum, AccountTypeEnum
from hooks import requires_auth
from resources import utils
from resources.base_resources import DAMCoreResource
from resources.schemas import SchemaUserToken
from settings import STATIC_DIRECTORY

mylogger = logging.getLogger(__name__)


class ResourceCreateUserToken(DAMCoreResource):
    def on_post(self, req, resp, *args, **kwargs):
        super(ResourceCreateUserToken, self).on_post(req, resp, *args, **kwargs)

        basic_auth_raw = req.get_header("Authorization")
        if basic_auth_raw is not None:
            basic_auth = basic_auth_raw.split()[1]
            auth_username, auth_password = (base64.b64decode(basic_auth).decode("utf-8").split(":"))
            if (auth_username is None) or (auth_password is None) or (auth_username == "") or (auth_password == ""):
                raise falcon.HTTPUnauthorized(description=messages.username_and_password_required)
        else:
            raise falcon.HTTPUnauthorized(description=messages.authorization_header_required)

        current_user = self.db_session.query(User).filter(User.email == auth_username).one_or_none()
        if current_user is None:
            current_user = self.db_session.query(User).filter(User.username == auth_username).one_or_none()

        if (current_user is not None) and (current_user.check_password(auth_password)):
            current_token = current_user.create_token()
            try:
                self.db_session.commit()
                resp.media = {"token": current_token.token}
                resp.status = falcon.HTTP_200
            except Exception as e:
                mylogger.critical("{}:{}".format(messages.error_saving_user_token, e))
                self.db_session.rollback()
                raise falcon.HTTPInternalServerError()
        else:
            raise falcon.HTTPUnauthorized(description=messages.user_not_found)


@falcon.before(requires_auth)
class ResourceDeleteUserToken(DAMCoreResource):
    @jsonschema.validate(SchemaUserToken)
    def on_post(self, req, resp, *args, **kwargs):
        super(ResourceDeleteUserToken, self).on_post(req, resp, *args, **kwargs)

        current_user = req.context["auth_user"]
        selected_token_string = req.media["token"]
        selected_token = self.db_session.query(UserToken).filter(UserToken.token == selected_token_string).one_or_none()

        if selected_token is not None:
            if selected_token.user.id == current_user.id:
                try:
                    self.db_session.delete(selected_token)
                    self.db_session.commit()

                    resp.status = falcon.HTTP_200
                except Exception as e:
                    mylogger.critical("{}:{}".format(messages.error_removing_user_token, e))
                    raise falcon.HTTPInternalServerError()
            else:
                raise falcon.HTTPUnauthorized(description=messages.token_doesnt_belongs_current_user)
        else:
            raise falcon.HTTPUnauthorized(description=messages.token_not_found)


@falcon.before(requires_auth)
class ResourceAccountUserProfile(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(ResourceAccountUserProfile, self).on_get(req, resp, *args, **kwargs)

        current_user = req.context["auth_user"]

        resp.media = current_user.json_model
        resp.status = falcon.HTTP_200


@falcon.before(requires_auth)
class ResourceAccountUpdateProfileImage(DAMCoreResource):
    def on_post(self, req, resp, *args, **kwargs):
        super(ResourceAccountUpdateProfileImage, self).on_post(req, resp, *args, **kwargs)

        # Get the user from the token
        current_user = req.context["auth_user"]
        resource_path = current_user.photo_path

        # Get the file from form
        incoming_file = req.get_param("image_file")

        # Run the common part for storing
        filename = utils.save_static_media_file(incoming_file, resource_path)

        # Update db model
        current_user.photo = filename
        self.db_session.add(current_user)
        self.db_session.commit()

        resp.status = falcon.HTTP_200


class ResourceAccountRecovery(DAMCoreResource):
    def on_post(self, req, resp, *args, **kwargs):
        super().on_post(req, resp, *args, **kwargs)

        email = req.media["email"]
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        try:
            aux_user = self.db_session.query(User).filter(User.email == email).one()
            aux_user.recovery_code = code
            self.db_session.add(aux_user)
            self.db_session.commit()

            # Enviar mail
            smtp_server = "smtp.gmeil.com"
            sender_email = "anoiagamers@gmail.com"
            password = ""

            html = """\
            <html>
            <head></head>
            <body>
                <p>Hi!<br>
                Your requested code to recover your account is:<br>
                """ + str(code) + """
                </p>
            </body>
            </html>
            """
            message = MIMEMultipart('alternative')
            message["Subject"]: "[MyApp] Recovery account instructions"
            message["From"]: sender_email
            message["To"]: email

            message.attach(MIMEText(html, "html"))
            try:
                server = smtplib.SMTP_SSL(smtp_server, 465)
                server.login(sender_email, password)
                server.sendmail(sender_email, email, message.as_string())
                server.quit()
            except Exception as e:
                print(e)
        except NoResultFound:
            resp.status = falcon.HTTP_200
        resp.status = falcon.HTTP_200


# update
@falcon.before(requires_auth)
class ResourceAccountUpdate(DAMCoreResource):
    def on_post(self, req, resp, *args, **kwargs):
        super().on_post(req, resp, *args, **kwargs)
        current_user = req.context["auth_user"]

        # bucle
        for i in req.media:
            valor = req.media[i]
            if i == "genere":
                valor = GenereEnum(valor.upper)
            elif i == "account_type":
                valor = AccountTypeEnum(valor.upper)
            setattr(current_user, i, valor)

        self.db_session.add(current_user)
        self.db_session.commit()

        resp.status = falcon.HTTP_200


@falcon.before(requires_auth)
class ResourceAccountDelete(DAMCoreResource):
    def on_delete(self, req, resp, *args, **kwargs):
        super(ResourceAccountDelete, self).on_delete(req, resp, *args, **kwargs)

        current_user = req.context["auth_user"]

        try:
            self.db_session.delete(current_user)
            self.db_session.commit()

            resp.status = falcon.HTTP_200
        except Exception as e:
            mylogger.critical("{}:{}".format(messages.error_removing_user, e))
            raise falcon.HTTPInternalServerError()
