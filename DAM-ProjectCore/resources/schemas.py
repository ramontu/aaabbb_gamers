#!/usr/bin/python
# -*- coding: utf-8 -*-

SchemaUserToken = {
    "type": "object",
    "properties": {
        "token": {"type": "string"},
    },
    "required": ["token"]
}

SchemaRegisterUser = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "pago": {"type": "string"},
        "email": {"type": "string"},
        "name": {"type": "string"},
        "surname": {"type": "string"},
        "genere": {"type": "string"}
    },
    "required": ["username", "password", "pago", "email", "name", "surname", "genere"]
}

SchemaUpdateUser = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "pago": {"type": "string"},
        "email": {"type": "string"},
        "name": {"type": "string"},
        "surname": {"type": "string"},
        "genere": {"type": "string"}
    }
}
