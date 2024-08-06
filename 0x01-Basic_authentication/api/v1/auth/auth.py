#!/usr/bin/env python3
"""
Module to manage Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required to access path
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
        Method that handles authorization header
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Validates current user
        """
        return None
