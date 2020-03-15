import copy
import json
import random

import pytest

from gilded_rose import Item, GildedRose


def item_encoder(obj):
    return obj.__dict__


@pytest.fixture
def items(num_items):
    items = []
    for _ in range(num_items):
        rand_num = random.randint(0, 99)
        sell_in = random.randint(-25, 99)
        quality = random.randint(0, 50)
        if rand_num < 5:
            item = Item(name="Sulfuras, Hand of Ragnaros", sell_in=sell_in, quality=80,)
        elif rand_num < 20:
            item = Item(
                name="Backstage passes to a TAFKAL80ETC concert",
                sell_in=sell_in,
                quality=quality,
            )
        elif rand_num < 30:
            item = Item(name="Aged Brie", sell_in=sell_in, quality=quality)
        else:
            item = Item(name="+5 Dexterity Vest", sell_in=sell_in, quality=quality)

        items.append(item)
    return items


@pytest.fixture
def items_new(items):
    return copy.deepcopy(items)


@pytest.fixture
def items_old(items):
    return copy.deepcopy(items)


@pytest.fixture
def days(num_days):
    return num_days


@pytest.fixture
def gilded_rose():
    return GildedRose([])


@pytest.fixture
def items_with_old_logic(items_old, days):
    items = []
    gr = GildedRose(items_old)
    for _ in range(days):
        for item in items_old:
            items.append(json.dumps(item, default=item_encoder))
        gr.update_quality_old()
    return items


@pytest.fixture
def items_with_new_logic(items_new, days):
    items = []
    gr = GildedRose(items_new)
    for _ in range(days):
        for item in items_new:
            items.append(json.dumps(item, default=item_encoder))
        gr.update_quality()
    return items


def test_update_item_default(gilded_rose):
    # normal conditions
    test_item = Item(name="+5 Dexterity Vest", sell_in=10, quality=10)
    item = gilded_rose.update_item_quality(copy.deepcopy(test_item))
    assert test_item.sell_in - 1 == item.sell_in
    assert test_item.quality - 1 == item.quality

    # passed sell in
    test_item = Item(name="+5 Dexterity Vest", sell_in=0, quality=10)
    item = gilded_rose.update_item_quality(copy.deepcopy(test_item))
    assert test_item.sell_in - 1 == item.sell_in
    assert test_item.quality - 2 == item.quality


def test_update_conjured_item(gilded_rose):
    # normal conditions
    test_item = Item(name="Conjured Mana Cake", sell_in=10, quality=10)
    item = gilded_rose.update_item_quality(copy.deepcopy(test_item))
    assert test_item.sell_in - 1 == item.sell_in
    assert test_item.quality - 2 == item.quality

    # passed sell in
    test_item = Item(name="Conjured Mana Cake", sell_in=0, quality=10)
    item = gilded_rose.update_item_quality(copy.deepcopy(test_item))
    assert test_item.sell_in - 1 == item.sell_in
    assert test_item.quality - 4 == item.quality


def test_backstage_pass_item(gilded_rose):
    # normal conditions
    test_item = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=11, quality=10,
    )
    item = gilded_rose.update_item_quality(copy.deepcopy(test_item))
    assert test_item.sell_in - 1 == item.sell_in
    assert test_item.quality + 1 == item.quality

    # less than 10 days left
    test_item = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=10,
    )
    item = gilded_rose.update_item_quality(copy.deepcopy(test_item))
    assert test_item.sell_in - 1 == item.sell_in
    assert test_item.quality + 2 == item.quality

    # less than 5 days
    test_item = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=10,
    )
    item = gilded_rose.update_item_quality(copy.deepcopy(test_item))
    assert test_item.sell_in - 1 == item.sell_in
    assert test_item.quality + 3 == item.quality

    # passed sell in
    test_item = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=10
    )
    item = gilded_rose.update_item_quality(copy.deepcopy(test_item))
    assert test_item.sell_in - 1 == item.sell_in
    assert 0 == item.quality


def test_legendary_item(gilded_rose):
    # all conditions
    test_item = Item(name="Sulfuras, Hand of Ragnaros", sell_in=26, quality=80,)
    item = gilded_rose.update_item_quality(copy.deepcopy(test_item))
    assert test_item.sell_in == item.sell_in
    assert 80 == item.quality


def test_update_quality_matches_old_logic(items_with_old_logic, items_with_new_logic):
    for i, item in enumerate(items_with_new_logic):
        assert items_with_old_logic[i] == item
