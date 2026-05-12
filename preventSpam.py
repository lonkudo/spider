import random
import time
from selenium.webdriver.common.action_chains import ActionChains

class MouseGlider:
    def __init__(self, driver):
        self.driver = driver
        self.mouse_pos = [0, 0]  # Assume starting at (0, 0)

    def glide_and_click(self, element, total_time=1.0, steps=20):
        # Ensure the element is in view
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", element)

        # Get element center
        rect = self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            return {
                x: rect.left + rect.width / 2,
                y: rect.top + rect.height / 2
            };
        """, element)

        end_x, end_y = rect["x"], rect["y"]
        start_x, start_y = self.mouse_pos
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps
        delay = total_time / steps

        # Now simulate a realistic glide
        for i in range(steps):
            move_x = start_x + dx * (i + 1)
            move_y = start_y + dy * (i + 1)

            self.driver.execute_script(
                "window.dispatchEvent(new MouseEvent('mousemove', {clientX: arguments[0], clientY: arguments[1]}));",
                move_x, move_y
            )
            time.sleep(random.uniform(delay * 0.8, delay * 1.2))

        # Move to and click the element with ActionChains (final motion)
        ActionChains(self.driver).move_to_element(element).pause(random.uniform(0.2, 0.4)).click().perform()

        # Update stored mouse position
        self.mouse_pos = [end_x, end_y]
