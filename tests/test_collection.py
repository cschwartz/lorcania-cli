import pytest
from lorcania_cli.api.lorcania import LorcaniaAPI
from lorcania_cli.collection import tabulate_collection


@pytest.mark.vcr()
def test_tabulate_collection(lorcania_api: LorcaniaAPI):
    table = tabulate_collection(lorcania_api)

    mickey_mouse_detective = table.loc[(1, 8, slice(None), slice(None))]
    assert len(mickey_mouse_detective) == 1
    assert (mickey_mouse_detective["op"] == 1).all()

    ariel_on_human_legs = table.loc[(2, 1, slice(None), slice(None))]
    assert len(ariel_on_human_legs) == 1
    assert (ariel_on_human_legs["regular"] == 2).all()

    cinderella_gentle_and_kind = table.loc[(2, 3, slice(None), slice(None))]
    assert len(cinderella_gentle_and_kind) == 1
    assert (cinderella_gentle_and_kind["foil"] == 2).all()
    assert (cinderella_gentle_and_kind["regular"] == 1).all()
