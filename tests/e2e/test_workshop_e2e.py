import re
from playwright.sync_api import expect

# PDFA 新建车辆用例（原样保留，这个一直是好的）
def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()


# PDFD 编辑车辆：创建 → 修改 → 保存 → 校验 → 刷新校验
def test_user_edits_car_and_change_survives_reload(page, live_server):
    # Step1：新建本田Civic
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_label("Color", exact=False).fill("Grey")
    page.get_by_role("button", name="Create car").click()

    # Step2：进入编辑页面
    page.get_by_role("link", name="Edit car").click()

    # Step3：选中原有文本，直接覆盖写入，【禁止fill("")清空】
    model_input = page.get_by_label("Model", exact=True)
    model_input.select_text()
    model_input.fill("Accord")

    year_input = page.get_by_label("Year", exact=True)
    year_input.select_text()
    year_input.fill("2023")

    # 等待保存按钮解除禁用，再点击提交
    save_btn = page.get_by_role("button", name="Save changes")
    expect(save_btn).to_be_enabled(timeout=5000)
    save_btn.click()

    # 等待页面跳转至详情页
    page.wait_for_url(re.compile(r"/cars/\d+$"), timeout=5000)

    # 校验页面包含Accord
    expect(page.get_by_text(re.compile("Accord"))).to_be_visible()

    # 刷新页面，验证持久化保存
    page.reload()
    expect(page.get_by_text(re.compile("Accord"))).to_be_visible()