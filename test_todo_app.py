import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

@pytest.fixture
def driver():
    chrome_options = Options()
    # Run headless in CI environment
    if os.environ.get('CI'):
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_add_task(driver):
    # Get the absolute path to the HTML file
    file_path = os.path.abspath("index.html")
    file_url = f"file://{file_path}"
    
    # Open the local HTML file
    driver.get(file_url)
    
    # Find the input field and add button
    input_field = driver.find_element(By.ID, "input")
    add_button = driver.find_element(By.ID, "add-btn")
    
    # Add a new task
    task_text = "Test Task 1"
    input_field.send_keys(task_text)
    add_button.click()
    
    # Check if the task was added to the list
    task_list = driver.find_element(By.ID, "task-list")
    task_items = task_list.find_elements(By.CLASS_NAME, "task-item")
    
    assert len(task_items) == 1
    
    # Find the span with class "text" inside the task item
    task_text_element = task_items[0].find_element(By.CLASS_NAME, "text")
    assert task_text_element.text == task_text

def test_complete_task(driver):
    # Get the absolute path to the HTML file
    file_path = os.path.abspath("index.html")
    file_url = f"file://{file_path}"
    
    # Open the local HTML file
    driver.get(file_url)
    
    # Add a task first
    input_field = driver.find_element(By.ID, "input")
    add_button = driver.find_element(By.ID, "add-btn")
    
    input_field.send_keys("Task to complete")
    add_button.click()
    
    # Find the most recently added task
    task_items = driver.find_elements(By.CLASS_NAME, "task-item")
    last_task = task_items[-1]
    
    # Click on the checkbox to mark it as complete
    check_button = last_task.find_element(By.CLASS_NAME, "btn-check")
    check_button.click()
    
    # Check if the task item has the 'active' class
    assert "active" in last_task.get_attribute("class")

def test_delete_task(driver):
    # Get the absolute path to the HTML file
    file_path = os.path.abspath("index.html")
    file_url = f"file://{file_path}"
    
    # Open the local HTML file
    driver.get(file_url)
    
    # Add a task first
    input_field = driver.find_element(By.ID, "input")
    add_button = driver.find_element(By.ID, "add-btn")
    
    input_field.send_keys("Task to delete")
    add_button.click()
    
    # Get the initial count of tasks
    initial_tasks = driver.find_elements(By.CLASS_NAME, "task-item")
    initial_count = len(initial_tasks)
    
    # Click on the close button of the last task to delete it
    close_button = initial_tasks[-1].find_element(By.CLASS_NAME, "btn-close")
    close_button.click()
    
    # Give it a moment to process
    time.sleep(0.5)
    
    # Get the new count of tasks
    updated_tasks = driver.find_elements(By.CLASS_NAME, "task-item")
    updated_count = len(updated_tasks)
    
    # Verify that a task was deleted
    assert updated_count == initial_count - 1