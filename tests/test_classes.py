import pytest
from src.classes import BaseProduct, Category, LawnGrass, Product, Smartphone


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


@pytest.fixture
def smartphone1():
    return Smartphone("Samsung Galaxy S23", "256GB", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый")


@pytest.fixture
def smartphone2():
    return Smartphone("Iphone 15", "512GB", 210000.0, 8, 98.2, "15", 512, "Gray space")


@pytest.fixture
def grass1():
    return LawnGrass("Газонная трава", "Элитная", 500.0, 20, "Россия", "7 дней", "Зеленый")


@pytest.fixture
def grass2():
    return LawnGrass("Газонная трава 2", "Выносливая", 450.0, 15, "США", "5 дней", "Темно-зеленый")


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
    capsys.readouterr()

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


def test_product_str(sample_product):
    assert str(sample_product) == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."


def test_category_str(sample_category):
    assert str(sample_category) == "Смартфоны, количество продуктов: 5 шт."


def test_product_add(sample_product):
    other_product = Product("Iphone 15", "512GB, Gray space", 210000.0, 2)
    assert sample_product + other_product == 1320000.0


def test_product_add_invalid(sample_product):
    with pytest.raises(TypeError):
        _ = sample_product + 100


def test_smartphone_init(smartphone1):
    assert smartphone1.name == "Samsung Galaxy S23"
    assert smartphone1.description == "256GB"
    assert smartphone1.price == 180000.0
    assert smartphone1.quantity == 5
    assert smartphone1.efficiency == 95.5
    assert smartphone1.model == "S23 Ultra"
    assert smartphone1.memory == 256
    assert smartphone1.color == "Серый"


def test_lawn_grass_init(grass1):
    assert grass1.name == "Газонная трава"
    assert grass1.description == "Элитная"
    assert grass1.price == 500.0
    assert grass1.quantity == 20
    assert grass1.country == "Россия"
    assert grass1.germination_period == "7 дней"
    assert grass1.color == "Зеленый"


def test_add_same_class_products(smartphone1, smartphone2, grass1, grass2):
    assert smartphone1 + smartphone2 == 2580000.0
    assert grass1 + grass2 == 16750.0


def test_add_different_class_products(smartphone1, grass1, sample_product):
    with pytest.raises(TypeError):
        _ = smartphone1 + grass1
    with pytest.raises(TypeError):
        _ = smartphone1 + sample_product


def test_category_add_valid_products(smartphone1, grass1):
    category = Category("Тест", "Описание", [smartphone1])
    category.add_product(grass1)
    assert len(category.products.splitlines()) == 2


def test_category_add_invalid_object():
    category = Category("Тест", "Описание", [])
    with pytest.raises(TypeError):
        category.add_product("Не продукт")
    with pytest.raises(TypeError):
        Category("Тест", "Описание", ["Не продукт"])


def test_print_mixin_product(capsys):
    Product("Телефон", "Описание", 10000.0, 5)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Product('Телефон', 'Описание', 10000.0, 5)"


def test_print_mixin_smartphone(capsys):
    Smartphone("iPhone", "Смартфон", 100000.0, 2, 95.5, "15 Pro", 256, "Титановый")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Smartphone('iPhone', 'Смартфон', 100000.0, 2)"


def test_print_mixin_lawn_grass(capsys):
    LawnGrass("Газон", "Трава", 500.0, 10, "Россия", "7 дней", "Зеленый")
    captured = capsys.readouterr()
    assert captured.out.strip() == "LawnGrass('Газон', 'Трава', 500.0, 10)"


def test_base_product_is_abstract():
    assert issubclass(Product, BaseProduct)
    with pytest.raises(TypeError):
        BaseProduct()


def test_product_zero_quantity():
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Бракованный товар", "Неизвестное описание", 1000.0, 0)


def test_category_middle_price(sample_category):
    assert sample_category.middle_price() == 180000.0

    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    sample_category.add_product(product2)
    assert sample_category.middle_price() == 195000.0


def test_category_middle_price_empty():
    empty_category = Category("Пустая категория", "Описание пустой категории", [])
    assert empty_category.middle_price() == 0
