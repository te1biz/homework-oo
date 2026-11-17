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


def test_category_init(sample_products):
    category = Category("Смартфоны", "Мобильные устройства", sample_products)
    assert category.name == "Смартфоны"
    assert category.description == "Мобильные устройства"
    assert len(category.products) == 2


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
