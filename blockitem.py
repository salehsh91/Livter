import pygame as pyg
from conster import *
from texture import *


class Item:
    items = {}

    def __init__(self, texture, type, name, damage=0, block=None):
        self.texture = texture
        self.type = type
        self.name = name
        self.damage = damage
        self.block = block

        self.items[name] = self

    @classmethod
    def getitem_status(cls, texture=None, type=None, name=None):
        for item in cls.items.values():

            if texture is not None and item.texture == texture:
                return item

            if type is not None and item.type == type:
                return item

            if name is not None and item.name == name:
                return item

        return None


class Block:
    blocks = {}

    def __init__(self, texture, type, name, damage=0, item=None):
        self.texture = texture
        self.type = type
        self.name = name
        self.damage = damage
        self.item = item

        self.blocks[name] = self

    @classmethod
    def getblock_status(cls, texture=None, type=None, name=None):
        for block in cls.blocks.values():

            if texture is not None and block.texture == texture:
                return block

            if type is not None and block.type == type:
                return block

            if name is not None and block.name == name:
                return block

        return None


water = Block(
    Texture.water,
    "water",
    "water",
    damage=0.5
)

sand = Block(
    Texture.sand,
    "sand",
    "sand"
)

stone = Block(
    Texture.stone,
    "stone",
    "stone"
)

grass = Block(
    Texture.grass,
    "grass",
    "grass"
)

plank = Block(
    Texture.plank,
    "plank",
    "plank"
)


Item(
    Texture.water,
    "water",
    "water",
    damage=0.5,
    block=water
)

Item(
    Texture.sand,
    "sand",
    "sand",
    block=sand
)

Item(
    Texture.stone,
    "stone",
    "stone",
    block=stone
)

Item(
    Texture.grass,
    "grass",
    "grass",
    block=grass
)

Item(
    Texture.plank,
    "plank",
    "plank",
    block=plank
)


water.item = Item.getitem_status(name="water")
sand.item = Item.getitem_status(name="sand")
stone.item = Item.getitem_status(name="stone")
grass.item = Item.getitem_status(name="grass")
plank.item = Item.getitem_status(name="plank")