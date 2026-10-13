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

    # 3.修改Model
    model_input = page.get_by_label("Model", exact=True)
    model_input.fill("")
    model_input.fill("Accord")

    # 年份number输入框，逐字符输入
    year_input = page.get_by_label("Year", exact=True)
    year_input.fill("")
    year_input.press_sequentially("2023")

    # 等待保存按钮启用，再点击
    save_btn = page.get_by_role("button", name="Save changes")
    expect(save_btn).to_be_enabled(timeout=5000)
    save_btn.click()
    
    # =========新增调试代码=========
    print("POST SUBMIT URL:", page.url)
    print(page.content())
    # ==============================

    # 4. 校验文本
    expect(page.get_by_text(re.compile("Accord"))).to_be_visible()

    # 5.刷新页面，确认修改依旧存在
    page.reload()
    expect(page.get_by_text(re.compile("Accord"))).to_be_visible()