#!/usr/bin/env python3

"""
API authentication module
"""
from os import getenv
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required
        """
        if path is None or not excluded_paths:
            return True
        for i in excluded_paths:
            if i.endswith('*') and path.startswith(i[:-1]):
                return False
            elif i in {path, path + '/'}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves authorization header
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns cookie value from a request
        """
        if request is None:
            return None

        return request.cookies.get(getenv('SESSION_NAME'))
