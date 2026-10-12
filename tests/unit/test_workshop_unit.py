from app.schemas import CarInput
import pytest
from pydantic import ValidationError

# 示例1（PDF原版，不能改动）
def test_car_text_fields_are_trimmed():
    car = CarInput(
        make=" Mazda ",
        model=" MX-5 ",
        year=2020,
        color=" Red ",
    )
    assert car.make == "Mazda"
    assert car.model == "MX-5"
    assert car.color == "Red"

# 自己写的测试，带WWP缩写
def test_WWP_blank_model_is_rejected():
    with pytest.raises(ValidationError):
        CarInput(make="Mazda", model=" ", year=2020)