import pytest
from src.classes import Product, Category


@pytest.fixture
def sample_product():
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)


@pytest.fixture
def sample_category(sample_product):
    Category.category_count = 0
    Category.product_count = 0
    return Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [sample_product],
    )


def test_product_init(sample_product):
    assert sample_product.name == "Samsung Galaxy S23 Ultra"
    assert sample_product.description == "256GB, Серый цвет, 200MP камера"
    assert sample_product.price == 180000.0
    assert sample_product.quantity == 5


def test_new_product():
    product_data = {
        "name": "Iphone 15",
        "description": "512GB, Gray space",
        "price": 210000.0,
        "quantity": 8,
    }
    product = Product.new_product(product_data)
    assert product.name == "Iphone 15"
    assert product.description == "512GB, Gray space"
    assert product.price == 210000.0
    assert product.quantity == 8


def test_price_setter_valid(sample_product):
    sample_product.price = 195000.0
    assert sample_product.price == 195000.0


def test_price_setter_invalid(sample_product, capsys):
    sample_product.price = 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "Цена не должна быть нулевая или отрицательная"
    assert sample_product.price == 180000.0

    sample_product.price = -500
    captured = capsys.readouterr()
    assert captured.out.strip() == "Цена не должна быть нулевая или отрицательная"
    assert sample_product.price == 180000.0


def test_category_init(sample_category):
    assert sample_category.name == "Смартфоны"
    assert Category.category_count == 1
    assert Category.product_count == 1


def test_category_products_getter(sample_category):
    expected = "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
    assert sample_category.products == expected


def test_add_product(sample_category):
    new_prod = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    sample_category.add_product(new_prod)
    assert Category.product_count == 2
    expected = (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт.\n"
    )
    assert sample_category.products == expected
