from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import gc

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.youtube.com/live_chat?v=KXe6CsjDXnk")

message_list = driver.find_elements(By.CSS_SELECTOR, 'yt-live-chat-text-message-renderer')

# Create a set to store the IDs of messages that have already been processed
processed_ids = set()

while True:
    # Get the latest list of messages
    message_list = driver.find_elements(By.CSS_SELECTOR, 'yt-live-chat-text-message-renderer')
    for message in message_list:
        # Get the ID of the message
        message_id = message.get_attribute('id')
        # Check if the message has already been processed
        if message_id not in processed_ids:
            # Find username
            username = message.find_element(By.CSS_SELECTOR, '#author-name').text
            # Check if username not empty
            # if username == "":
            #   time.sleep(1)
            #   username = message.find_element(By.CSS_SELECTOR, '#author-name').text
            # another solution
            # while username == "":
            #   username = message.find_element(By.CSS_SELECTOR, '#author-name').text
            # Find message
            msg = message.find_element(By.CSS_SELECTOR, '#message').text
            # Check if message not empty
            # If trying to retrieve the message again doesn't work either, then just have the for loop break out
            # and start from the beginning
            # if message == "":
            #   time.sleep(1)
            #   msg = message.find_element(By.CSS_SELECTOR, '#message').text
            # Name substitutions
            if username == "aqib mohammad":
                username = "aqua"
            if username == "Geome-TRY Ru Dasher?":
                username = "Geometry"
            
            # Commands
            # Uptime, how

            # Print the extracted data
            print(username,":",msg)

            # Add the message ID to the set of processed messages
            processed_ids.add(message_id)

    # Wait for 10 seconds before checking for new messages
    # time.sleep(1)
    gc.collect()

# Close the browser
driver.quit()