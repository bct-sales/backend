import pytest

from backend.db import models, orm
from backend.db.database import DatabaseSession
from backend.db.exceptions import *



@pytest.mark.parametrize("item_selection", [
    (1, ),
    (1, 2),
    (1, 2, 3, 4, 5),
    (5, 6, 7, 8, 9)
])
def test_create_sale(session: DatabaseSession,
                     items: list[models.Item],
                     item_selection: list[int]):
    sale_orm = session.create_sale(item_selection)
    assert set(item.item_id for item in sale_orm.items_sold) == set(item_selection)


def test_create_empty_sale(session: DatabaseSession):
    with pytest.raises(EmptySaleIsInvalid):
        session.create_sale([])


def test_create_sale_with_duplicate_items(session: DatabaseSession,
                                          items: list[models.Item],):
    with pytest.raises(DuplicateItemsInSale):
        session.create_sale([items[0].item_id, items[0].item_id])


def test_create_sale_with_nonexisting_item(session: DatabaseSession,
                                           items: list[models.Item],):
    nonexisting_item_id = max(item.item_id for item in items) + 1
    with pytest.raises(UnknownItemException):
        session.create_sale([nonexisting_item_id])


@pytest.mark.parametrize("item_selections", [
    [[1]],
    [[1, 2]],
    [[1], [2]],
    [[1], [2], [3], [4], [5]],
    [[1, 3], [5, 6, 9], [14, 16, 19], [22, 24]]
])
def test_collect_sold_items(session: DatabaseSession,
                            items: list[models.Item],
                            item_selections: list[list[int]]):
    for item_selection in item_selections:
        session.create_sale(item_selection)
    expected = set(x for xs in item_selections for x in xs)
    actual = set(session.collect_sold_items())
    assert expected == actual
