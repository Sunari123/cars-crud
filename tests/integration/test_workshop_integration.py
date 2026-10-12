from app import database
from app.schemas import CarInput

# 示例2（PDF原版，不动）
def test_saved_car_can_be_read_from_sqlite(database_path):
    database.initialize(database_path)
    saved = database.create_car(
        database_path,
        CarInput(make="Toyota", model="Yaris", year=2020, color="Blue")
    )
    loaded = database.get_car(database_path, saved.id)

    assert loaded is not None
    assert loaded.id == saved.id
    assert loaded.make == "Toyota"
    assert loaded.year == 2020

# 自己写的测试，WWP缩写
def test_WWP_deleting_one_car_keeps_other(database_path):
    database.initialize(database_path)
    car1 = database.create_car(
        database_path,
        CarInput(make="Honda", model="Civic", year=2021, color="Black")
    )
    car2 = database.create_car(
        database_path,
        CarInput(make="BMW", model="3 Series", year=2022, color="White")
    )

    database.delete_car(database_path, car1.id)

    assert database.get_car(database_path, car1.id) is None
    assert database.get_car(database_path, car2.id) is not None

    car_list = database.list_cars(database_path)
    assert len(car_list) == 1
    assert car_list[0].id == car2.id