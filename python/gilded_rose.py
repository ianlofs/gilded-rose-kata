import warnings


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_item_quality(self, item):
        """update_item_quality updates an items quality
        and decrements it's sell_in value.

        :param item: The item to update
        :type item: Item
        :return: The updated item
        :rtype: Item
        """
        # legendary items
        if item.name == "Sulfuras, Hand of Ragnaros":
            item.quality = 80
            return item

        item.sell_in -= 1
        item_name = item.name.lower().strip()

        multiplier = -1  # default

        if "aged brie" in item_name:
            multiplier = 1

        if "backstage" in item_name:
            multiplier = 1
            if item.sell_in < 0:
                multiplier = -item.quality
            elif item.sell_in < 5:
                multiplier = 3
            elif item.sell_in < 10:
                multiplier = 2

        if "conjured" in item_name:
            multiplier = -2

        # update quality
        item.quality += multiplier

        # double after 0
        if item.sell_in < 0:
            item.quality += multiplier

        # enforce bounds
        if item.quality > 50:
            item.quality = 50

        if item.quality < 0:
            item.quality = 0

        return item

    def update_quality(self):
        """update_quality Updates the quality of all the
        items for sale at the Guilded Rose once a day.
        """
        for i, item in enumerate(self.items):
            self.items[i] = self.update_item_quality(item)

    def update_quality_old(self):
        warning = (
            "\nThis only contains logic for backstage passes, legendary items, aged brie, and regular items.\n"
            + "Please use the GildedRose().update_qualify method instead."
        )
        warnings.warn(warning, DeprecationWarning)
        for item in self.items:
            if (
                item.name != "Aged Brie"
                and item.name != "Backstage passes to a TAFKAL80ETC concert"
            ):
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
