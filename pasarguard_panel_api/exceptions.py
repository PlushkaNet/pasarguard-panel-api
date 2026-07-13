"""
Custom exception classes used internally within the SDK.

These exceptions are not intended to be raised directly by end-users
of the SDK, but are used for internal control flow, error handling,
and to provide meaningful error messages for internal components.

All exceptions in this module inherit from a common base to allow
for consistent internal error handling.
"""

class PasarguardError(Exception):
    """Base class for all exceptions with panel inside this SDK"""

class AuthorizationError(PasarguardError):
    """Exception that represents error with authentication"""

class UserAlreadyExistsError(PasarguardError):
    """
    Exception that represents HTTP 409 (Conflict) from
    Pasarguard panel API when trying to add user.
    """

class APIResponseError(PasarguardError):
    """Exception for non-200 and non-201 response status codes from Pasarguard API"""
