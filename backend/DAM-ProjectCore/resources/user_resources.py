#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import logging
import tokenize

import falcon
from falcon.media.validators import jsonschema
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from resources import utils
import messages
from db.models import User, GenereEnum, AccountTypeEnum, Matching_data
from hooks import requires_auth
from resources.base_resources import DAMCoreResource
from resources.matching.matching_resources import recalculate_score
from resources.schemas import SchemaRegisterUser


mylogger = logging.getLogger(__name__)



class ResourceGetUserProfile(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(ResourceGetUserProfile, self).on_get(req, resp, *args, **kwargs)
        if "username" in kwargs:
            try:
                aux_user = self.db_session.query(User).filter(User.username == kwargs["username"]).one()

                resp.media = aux_user.public_profile
                resp.status = falcon.HTTP_200
            except NoResultFound:
                raise falcon.HTTPBadRequest(description=messages.user_not_found)


class ResourceRegisterUser(DAMCoreResource):
    @jsonschema.validate(SchemaRegisterUser)
    def on_post(self, req, resp, *args, **kwargs):
        super(ResourceRegisterUser, self).on_post(req, resp, *args, **kwargs)

        aux_user = User()

        try:
            aux_user.username = req.media["username"]
            aux_user.password = req.media["password"]
            aux_user.email = req.media["email"]
            toke = req.media["birthday"].split("/")
            aux_user.birthday = datetime.datetime(int(toke[2]), int(toke[1]), int(toke[0]), 0, 0, 1)
            self.db_session.add(aux_user)

            try:
                self.db_session.commit()
                recalculate_score(aux_user)
            except IntegrityError:
                raise falcon.HTTPBadRequest(description=messages.user_exists)

        except KeyError:
            raise falcon.HTTPBadRequest(description="user_resources(): Parametres incorrectes")

        resp.status = falcon.HTTP_200


# TODO comprovar que funciona
# Sera substituida per una altra fuciona a common resources
@falcon.before(requires_auth)
class DownloadUserImage(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(DownloadUserImage, self).on_get(req, resp, *args, **kwargs)
        # Get the user from the token
        current_user = req.context["auth_user"]

        # Run the common part for reading
        file = utils.get_static_media_file(current_user.photo_path)
        resp.media = file
        resp.status = falcon.HTTP_200


@falcon.before(requires_auth)
class DownloadMenuInfo(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(DownloadMenuInfo, self).on_get(req, resp, *args, **kwargs)
        current_user = req.context["auth_user"]

        file = utils.get_static_media_file(current_user.photo_path)
        resp.media = [file, current_user.username]
        resp.status = falcon.HTTP_200
