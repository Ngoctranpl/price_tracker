from tracker import get_price , save
import pytest


def test_price_extraction():
    assert get_price("https://www.mohito.com/pl/pl/cekinowa-sukienka-mini-667fv-gld")   == (269.99, "PLN")

    with pytest.raises(SystemExit):
        get_price("https://www.mohito.com/pl/pl/sukienka-maxi-z-wiskozy-2-668fv-08pm")  # invalid URL
  