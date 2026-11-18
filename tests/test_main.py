import pytest

from src.classes import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counts():
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_product():
    return Product("Samsung Galaxy S23", "Флагман", 180000.0, 5)


@pytest.fixture
def sample_products():
    return [
        Product("Samsung Galaxy S23", "Флагман", 180000.0, 5),
        Product("Iphone 15", "Смартфон Apple", 110000.0, 8),
    ]


def test_product_init(sample_product):
    assert sample_product.name == "Samsung Galaxy S23"
    assert sample_product.description == "Флагман"
    assert sample_product.price == 180000.0
    assert sample_product.quantity == 5


def test_new_product():
    product_data = {
        "name": "Xiaomi Redmi Note 11",
        "description": "1024GB, Синий",
        "price": 31000.0,
        "quantity": 14,
    }
    product = Product.new_product(product_data)
    assert product.name == "Xiaomi Redmi Note 11"
    assert product.description == "1024GB, Синий"
    assert product.price == 31000.0
    assert product.quantity == 14


def test_price_setter_valid(sample_product):
    sample_product.price = 190000.0
    assert sample_product.price == 190000.0


def test_price_setter_invalid(sample_product, capsys):
    sample_product.price = 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "Цена не должна быть нулевая или отрицательная"
    assert sample_product.price == 180000.0

    sample_product.price = -100
    captured = capsys.readouterr()
    assert captured.out.strip() == "Цена не должна быть нулевая или отрицательная"
    assert sample_product.price == 180000.0


def test_category_init(sample_products):
    category = Category("Смартфоны", "Мобильные устройства", sample_products)
    assert category.name == "Смартфоны"
    assert category.description == "Мобильные устройства"
    expected_products = (
        "Samsung Galaxy S23, 180000.0 руб. Остаток: 5 шт.\n"
        "Iphone 15, 110000.0 руб. Остаток: 8 шт.\n"
    )
    assert category.products == expected_products


def test_category_counters(sample_products):
    assert Category.category_count == 0
    assert Category.product_count == 0

    category1 = Category("Смартфоны", "Категория 1", sample_products)
    assert Category.category_count == 1
    assert Category.product_count == 2
    assert category1.category_count == 1

    category2 = Category("Телевизоры", "Категория 2", [sample_products[0]])
    assert Category.category_count == 2
    assert Category.product_count == 3
    assert category2.category_count == 2


def test_add_product(sample_products, sample_product):
    category = Category("Смартфоны", "Мобильные устройства", sample_products)
    assert Category.product_count == 2

    category.add_product(sample_product)
    assert Category.product_count == 3
    expected_products = (
        "Samsung Galaxy S23, 180000.0 руб. Остаток: 5 шт.\n"
        "Iphone 15, 110000.0 руб. Остаток: 8 шт.\n"
        "Samsung Galaxy S23, 180000.0 руб. Остаток: 5 шт.\n"
    )
    assert category.products == expected_products
