from unittest.mock import Mock

import pytest

from praktikum.burger import Burger
from praktikum.ingredient_types import (
    INGREDIENT_TYPE_FILLING,
    INGREDIENT_TYPE_SAUCE
)


@pytest.fixture
def burger():
    return Burger()


@pytest.fixture
def bun():
    bun = Mock()
    bun.get_name.return_value = 'black bun'
    bun.get_price.return_value = 100
    return bun


def test_set_buns_sets_bun(burger, bun):
    burger.set_buns(bun)

    assert burger.bun == bun


def test_add_ingredient_adds_ingredient_to_list(burger):
    ingredient = Mock()

    burger.add_ingredient(ingredient)

    assert ingredient in burger.ingredients


def test_remove_ingredient_removes_ingredient_from_list(burger):
    ingredient = Mock()
    burger.add_ingredient(ingredient)

    burger.remove_ingredient(0)

    assert ingredient not in burger.ingredients


def test_remove_ingredient_with_invalid_index_raises_index_error(burger):
    with pytest.raises(IndexError):
        burger.remove_ingredient(0)


def test_move_ingredient_changes_order_of_ingredients(burger):
    ingredient_1 = Mock()
    ingredient_2 = Mock()

    burger.add_ingredient(ingredient_1)
    burger.add_ingredient(ingredient_2)

    burger.move_ingredient(0, 1)

    assert burger.ingredients == [ingredient_2, ingredient_1]


def test_move_ingredient_with_invalid_index_raises_index_error(burger):
    with pytest.raises(IndexError):
        burger.move_ingredient(0, 1)


@pytest.mark.parametrize(
    'ingredient_prices, expected_price',
    [
        ([], 200),
        ([50], 250),
        ([50, 30], 280)
    ]
)
def test_get_price_returns_correct_price(
        burger,
        bun,
        ingredient_prices,
        expected_price
):
    burger.set_buns(bun)

    for price in ingredient_prices:
        ingredient = Mock()
        ingredient.get_price.return_value = price
        burger.add_ingredient(ingredient)

    assert burger.get_price() == expected_price


def test_get_receipt_returns_correct_receipt(burger, bun):
    burger.set_buns(bun)

    sauce = Mock()
    sauce.get_type.return_value = INGREDIENT_TYPE_SAUCE
    sauce.get_name.return_value = 'hot sauce'
    sauce.get_price.return_value = 20

    filling = Mock()
    filling.get_type.return_value = INGREDIENT_TYPE_FILLING
    filling.get_name.return_value = 'cutlet'
    filling.get_price.return_value = 50

    burger.add_ingredient(sauce)
    burger.add_ingredient(filling)

    expected_receipt = (
        '(==== black bun ====)\n'
        '= sauce hot sauce =\n'
        '= filling cutlet =\n'
        '(==== black bun ====)\n\n'
        'Price: 270'
    )

    assert burger.get_receipt() == expected_receipt
    