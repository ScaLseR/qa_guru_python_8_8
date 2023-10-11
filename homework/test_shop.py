"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from random import randint
from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture()
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    @pytest.mark.parametrize("quantity", [0, 1, 999, 1000])
    def test_product_check_quantity(self, product, quantity):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(quantity)

    def test_product_check_quantity_err(self, product):
        assert not product.check_quantity(1001)

    @pytest.mark.parametrize("count, actual_quantity", [(0, 1000), (1, 999), (999, 1), (1000, 0)])
    def test_product_buy(self, product, count, actual_quantity):
        # TODO напишите проверки на метод buy
        product.buy(count)
        assert product.quantity == actual_quantity

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    @pytest.mark.parametrize("actual_quantity, expected_quantity", [(0, 0), (1, 1), (10, 10)])
    def test_products_add_to_cart(self, cart, product, actual_quantity, expected_quantity):
        cart.add_product(product, actual_quantity)
        assert cart.products[product] == expected_quantity
        add_count = randint(0, 100)
        cart.add_product(product, add_count)
        assert cart.products[product] == expected_quantity + add_count

    @pytest.mark.parametrize("add_products, rm_products, expected_count", [(11, 1, 10), (10, 1, 9)])
    def test_products_del_from_cart(self, cart, product, add_products, rm_products, expected_count):
        cart.add_product(product, add_products)
        cart.remove_product(product, rm_products)
        assert cart.products[product] == expected_count

    @pytest.mark.parametrize("add_products, rm_products", [(0, 0), (1, 1), (0, 1)])
    def test_products_del_from_cart_all(self, cart, product, add_products, rm_products):
        cart.add_product(product, add_products)
        cart.remove_product(product, rm_products)
        assert product not in cart.products.keys()

    @pytest.mark.parametrize("quantity", [0, 1, 999, 1000])
    def test_cart_clear(self, cart, product, quantity):
        cart.add_product(product, quantity)
        cart.clear()
        assert product not in cart.products.keys()

    @pytest.mark.parametrize("quantity", [0, 1, 999, 1000])
    def test_cart_get_total_price(self, cart, product, quantity):
        cart.add_product(product, quantity)
        assert cart.get_total_price() == product.price * quantity
