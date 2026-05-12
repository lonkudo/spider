import os

folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages')

def save_page(driver, name="page"):
    """
    Save current page HTML and screenshot using Selenium WebDriver.

    Args:
        driver: Selenium WebDriver instance
        name (str): Base name for saved files
        folder (str): Folder to save the files in
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    html_path = os.path.join(folder, f"{name}.html")
    screenshot_path = os.path.join(folder, f"{name}.png")

    # Save HTML
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    # Save screenshot
    driver.save_screenshot(screenshot_path)

    print(f"✅ Saved HTML to: {html_path}")
    print(f"✅ Saved Screenshot to: {screenshot_path}")
