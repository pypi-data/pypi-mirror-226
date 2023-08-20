class AuthenticationError(Exception):
    """Exception raised when authentication has been attempted and denied.
    """
    pass


class OauthError(Exception):
    pass


class CredentialsError(OauthError):
    """Exception raised when authentication params are missing or have invalid format.
    """
    pass


class AlienMatterError(Exception):
    """Attempt to authorize or authenticate against a resource not sufficiently trusted
    """
    pass


class ChallengeError(Exception):
    """A challenge is invalid or used in an invalid context
    """
    pass
