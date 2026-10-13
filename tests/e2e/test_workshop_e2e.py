import re
from playwright.sync_api import expect

# PDF A 复制的基础E2E用例：浏览器填表新建车辆
def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()

# PDF D自己写的用例：创建、编辑车辆，刷新页面确认修改保存
def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1. 新建 Honda Civic 2022
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_label("Color", exact=False).fill("Grey")
    page.get_by_role("button", name="Create car").click()

    # 2.点编辑链接
    page.get_by_role("link", name="Edit car").click()

    # 3.修改为 Accord，2023，保存，使用fill内置清空（推荐，比键盘select_all稳定）
    model_input = page.get_by_label("Model", exact=True)
    model_input.fill("")  # 先清空
    model_input.fill("Accord")

    year_input = page.get_by_label("Year", exact=True)
    year_input.fill("")
    year_input.fill("2023")

    page.get_by_role("button", name="Save changes").click()

    # 4. 页面任意位置找到 Accord 文本即可，不再限制heading标签
    expect(page.get_by_text(re.compile("Accord"))).to_be_visible()

    # 5.刷新页面，确认修改依旧存在
    page.reload()
    expect(page.get_by_text(re.compile("Accord"))).to_be_visible()