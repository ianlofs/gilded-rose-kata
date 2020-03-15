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
        quality = random.randint(-25, 99)
        if rand_num < 5:
            item = Item(name="Sulfuras, Hand of Ragnaros", sell_in=sell_in, quality=quality,)
        elif rand_num < 20:
            item = Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=sell_in, quality=quality,)
        elif rand_num < 50:
            item = Item(name="Conjured Mana Cake", sell_in=sell_in, quality=quality)
            if rand_num % 2 == 0:
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
def items_with_old_logic(items_old, days):
    items_with_old_logic_lines = []
    for _ in range(days):
        for item in items_old:
            item = json.dumps(item, default=item_encoder)
            items_with_old_logic_lines.append(item)
        GildedRose(items_old).update_quality_old()
    return items_with_old_logic_lines


@pytest.fixture
def items_with_new_logic(items_new, days):
    items_with_new_logic_lines = []
    for _ in range(days):
        for item in items_new:
            item = json.dumps(item, default=item_encoder)
            items_with_new_logic_lines.append(item)
        GildedRose(items_new).update_quality()
    return items_with_new_logic_lines


def test_update_quality(items_with_old_logic, items_with_new_logic):
    for i, item in enumerate(items_with_new_logic):
        assert items_with_old_logic[i] == item
