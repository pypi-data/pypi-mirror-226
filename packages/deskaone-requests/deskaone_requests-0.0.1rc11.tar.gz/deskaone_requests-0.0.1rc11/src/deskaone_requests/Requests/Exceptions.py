# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------- #

"""
cloudscraper.exceptions
~~~~~~~~~~~~~~~~~~~
This module contains the set of cloudscraper exceptions.
"""

# ------------------------------------------------------------------------------- #


class CloudException(Exception):
    """
    Base exception class for cloudscraper for Cloud
    """


class CloudLoopProtection(CloudException):
    """
    Raise an exception for recursive depth protection
    """


class CloudCode1020(CloudException):
    """
    Raise an exception for Cloud code 1020 block
    """


class CloudIUAMError(CloudException):
    """
    Raise an error for problem extracting IUAM paramters
    from Cloud payload
    """


class CloudChallengeError(CloudException):
    """
    Raise an error when detected new Cloud challenge
    """


class CloudSolveError(CloudException):
    """
    Raise an error when issue with solving Cloud challenge
    """


class CloudCaptchaError(CloudException):
    """
    Raise an error for problem extracting Captcha paramters
    from Cloud payload
    """


class CloudCaptchaProvider(CloudException):
    """
    Raise an exception for no Captcha provider loaded for Cloud.
    """

# ------------------------------------------------------------------------------- #


class CaptchaException(Exception):
    """
    Base exception class for cloudscraper captcha Providers
    """


class CaptchaServiceUnavailable(CaptchaException):
    """
    Raise an exception for external services that cannot be reached
    """


class CaptchaAPIError(CaptchaException):
    """
    Raise an error for error from API response.
    """


class CaptchaAccountError(CaptchaException):
    """
    Raise an error for captcha provider account problem.
    """


class CaptchaTimeout(CaptchaException):
    """
    Raise an exception for captcha provider taking too long.
    """


class CaptchaParameter(CaptchaException):
    """
    Raise an exception for bad or missing Parameter.
    """


class CaptchaBadJobID(CaptchaException):
    """
    Raise an exception for invalid job id.
    """


class CaptchaReportError(CaptchaException):
    """
    Raise an error for captcha provider unable to report bad solve.
    """
