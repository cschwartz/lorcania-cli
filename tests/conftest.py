import dataclasses
import os
from typing import Any, Dict, List
from dotenv import load_dotenv, find_dotenv
import pytest
from http.cookies import SimpleCookie
from lorcania_cli.api.lorcania import LorcaniaAPI
import vcr  # type: ignore


@pytest.fixture(scope="module")
def vcr_config():
    cookies_to_sanitize = [
        CookieEntry("XSRF-TOKEN", "DUMMY"),
        CookieEntry(
            "lorcania_lorcana_cards_decks_collection_news_and_prices_session", "DUMMY"
        ),
    ]

    return {
        "filter_headers": [("X-XSRF-TOKEN", "DUMMY")],
        "filter_post_data_parameters": [
            ("email", "email@example.com"),
            ("password", "password"),
        ],
        "before_record_request": sanitize_cookie_in_request(cookies_to_sanitize),
        "before_record_response": sanitize_cookie_in_response(cookies_to_sanitize),
    }


@pytest.fixture(scope="session", autouse=True)
def load_env():
    env_file = find_dotenv(".env.tests")
    load_dotenv(env_file, override=True)


@pytest.fixture(scope="session")
def lorcania_api():
    email = os.environ["LORCANIA_EMAIL"]
    password = os.environ["LORCANIA_PASSWORD"]
    return LorcaniaAPI(email, password)


@dataclasses.dataclass
class CookieEntry:
    name: str
    value: str


def sanitize_cookie_in_request(to_sanitize: List[CookieEntry]):
    def f(request: vcr.request.Request):
        if cookie_str := request.headers.get("Cookie"):
            sanitized_cookie = sanitize_cookie(cookie_str, to_sanitize)

            request.headers["Cookie"] = "; ".join(sanitized_cookie)

        return request

    return f


def sanitize_cookie_in_response(to_sanitize: List[CookieEntry]):
    def f(response: Dict[str, Any]):
        if cookie_strs := response["headers"].get("Set-Cookie"):
            cookie_str = "; ".join(cookie_strs)
            sanitized_cookie = sanitize_cookie(cookie_str, to_sanitize)
            response["headers"]["Set-Cookie"] = sanitized_cookie

        return response

    return f


def sanitize_cookie(cookie_str: str, cookies_to_sanitize: List[CookieEntry]):
    simple_cookie: SimpleCookie = SimpleCookie(cookie_str)

    for cookie_to_sanitize in cookies_to_sanitize:
        if cookie := simple_cookie.get(cookie_to_sanitize.name):
            cookie.set(
                cookie_to_sanitize.name,
                *simple_cookie.value_encode(cookie_to_sanitize.value),
            )

    return [v.OutputString() for v in simple_cookie.values()]
