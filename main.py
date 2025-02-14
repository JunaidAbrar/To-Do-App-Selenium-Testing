from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

def run_todo_app_tests():
    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    
    try:
        # Get the absolute path to the HTML file
        file_path = os.path.abspath("index.html")
        file_url = f"file://{file_path}"
        
        # Open the local HTML file
        driver.get(file_url)
        time.sleep(1)  # Wait to see the initial page
        
        # Test: Add a task
        print("Testing: Add a task")
        input_field = driver.find_element(By.ID, "input")
        add_button = driver.find_element(By.ID, "add-btn")
        
        task_text = "Test Task 1"
        input_field.send_keys(task_text)
        time.sleep(1)  # Wait to see the text being entered
        add_button.click()
        time.sleep(1)  # Wait to see the task being added
        
        task_list = driver.find_element(By.ID, "task-list")
        task_items = task_list.find_elements(By.CLASS_NAME, "task-item")
        
        if len(task_items) == 1:
            task_text_element = task_items[0].find_element(By.CLASS_NAME, "text")
            if task_text_element.text == task_text:
                print("✅ Add task test passed!")
            else:
                print("❌ Add task test failed: Text doesn't match")
        else:
            print(f"❌ Add task test failed: Expected 1 task, found {len(task_items)}")
        
        # Test: Complete a task
        print("\nTesting: Complete a task")
        check_button = task_items[0].find_element(By.CLASS_NAME, "btn-check")
        check_button.click()
        time.sleep(1)  # Wait to see the task being completed
        
        if "active" in task_items[0].get_attribute("class"):
            print("✅ Complete task test passed!")
        else:
            print("❌ Complete task test failed: Task not marked as active")
        
        # Test: Delete a task
        print("\nTesting: Delete a task")
        initial_count = len(task_items)
        close_button = task_items[0].find_element(By.CLASS_NAME, "btn-close")
        close_button.click()
        time.sleep(1)  # Wait to see the task being deleted
        
        updated_tasks = driver.find_elements(By.CLASS_NAME, "task-item")
        
        if len(updated_tasks) == initial_count - 1:
            print("✅ Delete task test passed!")
        else:
            print(f"❌ Delete task test failed: Expected {initial_count - 1} tasks, found {len(updated_tasks)}")
            
        # Keep the browser open for a few seconds so you can see the final state
        time.sleep(5)
            
    finally:
        # Close the browser
        driver.quit()
        
if __name__ == "__main__":
    run_todo_app_tests()