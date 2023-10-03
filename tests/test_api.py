import pytest
import os

from lorcania_cli.api import LorcaniaAPI, AuthenticationError


@pytest.mark.vcr()
def test_login_fails():
    email = os.environ["LORCANIA_EMAIL"]
    with (pytest.raises(AuthenticationError)):
        LorcaniaAPI(email, "not_the_password")


@pytest.mark.vcr()
def test_login_succeeds(lorcania_api: LorcaniaAPI):
    assert lorcania_api


@pytest.mark.vcr()
def test_cards(lorcania_api: LorcaniaAPI):
    cards = lorcania_api.cards()
    assert "cards" in cards


@pytest.mark.vcr()
def test_collection(lorcania_api: LorcaniaAPI):
    collection = lorcania_api.collection()
    assert "collection" in collection
