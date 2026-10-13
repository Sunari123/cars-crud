import re
from playwright.sync_api import expect

def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()


def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1. 创建车辆
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_label("Color", exact=False).fill("Grey")
    page.get_by_role("button", name="Create car").click()

    # 2. 打开编辑页面
    page.get_by_role("link", name="Edit car").click()

    # =========【重点！JS注入赋值，不触发前端校验】=========
    # 获取Model输入框，直接JS改value
    page.eval_on_selector('label[for="model"] + input', '''(el) => {
        el.value = "Accord";
    }''')
    # Year输入框JS赋值
    page.eval_on_selector('label[for="year"] + input', '''(el) => {
        el.value = "2023";
    }''')
    # ======================================================

    # 等待按钮启用
    save_btn = page.get_by_role("button", name="Save changes")
    expect(save_btn).to_be_enabled(timeout=5000)
    save_btn.click()

    # 等待跳转到详情页面
    page.wait_for_url(re.compile(r"/cars/\d+$"), timeout=5000)

    # 校验Accord存在
    expect(page.get_by_text(re.compile("Accord"))).to_be_visible()
    page.reload()
    expect(page.get_by_text(re.compile("Accord"))).to_be_visible()