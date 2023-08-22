from sempy.fabric._environment import _get_environment

from abc import ABC, abstractmethod
import datetime
import jwt
import time


class TokenProvider(ABC):
    """
    Abstract base class for logic that acquires auth tokens.
    """
    @abstractmethod
    def __call__(self) -> str:
        """
        Get implementation specific token.

        Returns
        -------
        str
            Auth token.
        """
        raise NotImplementedError


class ConstantTokenProvider(TokenProvider):
    """
    Wrapper around a token that was externally acquired by the user.

    Parameters
    ----------
    token : str
        Token that will be supplied upon requst.
    """
    def __init__(self, token):
        self.token = token

    def __call__(self):
        """
        Get token.

        Returns
        -------
        str
            Fixed token provided by user during instantiation.
        """
        return self.token


class SynapseTokenProvider(TokenProvider):
    """
    Acquire an auth token from within a Trident workspace.
    """
    def __call__(self):
        """
        Get token from within a Trident workspace.

        Returns
        -------
        str
            Token acquired from Trident libraries.
        """
        try:
            from trident_token_library_wrapper import PyTridentTokenLibrary
            return PyTridentTokenLibrary.get_access_token("pbi")
        except ImportError:
            raise RuntimeError("No token_provider specified and unable to obtain token from the environment")


class _UninitializedTokenProvider(TokenProvider):
    """
    Default dummy token provider used when no suitable token could be automatically retrieved.
    """
    def __call__(self):
        """
        Throw exception signalling the need for manual token initialization.

        Returns
        -------
        None
            Throws an exception when used.
        """
        raise RuntimeError("No token_provider specified and unable to obtain token from the environment")


def _create_default_token_provider() -> TokenProvider:
    # Choosing to use _get_environment for consistency.
    if _get_environment() == "local":
        return _UninitializedTokenProvider()
    else:
        return SynapseTokenProvider()


def _get_token_expiry_raw_timestamp(token: str) -> int:
    payload = jwt.decode(token, options={"verify_signature": False})
    return payload.get("exp", 0)


def _get_token_seconds_remaining(token: str) -> int:
    exp_time = _get_token_expiry_raw_timestamp(token)
    now = int(time.time())
    return exp_time - now


def _get_token_expiry_utc(token: str) -> str:
    exp_time = _get_token_expiry_raw_timestamp(token)
    return str(datetime.datetime.utcfromtimestamp(exp_time))
