import re
from playwright.sync_api import Page, expect

def test_user_edits_car_and_change_survives_reload(page: Page, live_server):
    # 1. 创建车辆
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_label("Color", exact=False).fill("Grey")
    page.get_by_role("button", name="Create car").click()

    # 2. 打开编辑页面
    page.get_by_role("link", name="Edit car").click()
    page.wait_for_load_state("domcontentloaded")

    # 清空原有内容，模拟真人打字
    model_input = page.get_by_label("Model")
    model_input.select_text()
    model_input.type("Accord")
    model_input.blur()

    year_input = page.get_by_label("Year")
    year_input.select_text()
    year_input.type("2023")
    year_input.blur()

    # 保存
    save_btn = page.get_by_role("button", name="Save changes")
    expect(save_btn).to_be_enabled(timeout=5000)
    save_btn.click()

    # 等待跳转详情页
    page.wait_for_url(re.compile(r"/cars/\d+$"), timeout=5000)

 # 直接根据id定位model字段
    expect(page.locator("#car-model")).to_have_text("Accord")
    page.reload()
    expect(page.locator("#car-model")).to_have_text("Accord")