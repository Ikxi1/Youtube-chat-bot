from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import re
import time
import gc

a = 0

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.youtube.com/live_chat?v=MdpFYmrtMLk")

message_list = driver.find_elements(By.CSS_SELECTOR, 'yt-live-chat-text-message-renderer')

processed_ids = set()

with open('blocked_words.txt', 'r') as f:
    blocked_words = [line.strip() for line in f]
    
with open("commands.txt", "r") as f:
    commands = {}
    for line in f:
        parts = line.strip().split(";")
        command = parts[0]
        text = parts[1] if len(parts) > 1 else ""
        commands[command] = text

# Put code to enable timestamps

while True:
    # Get the latest list of messages
    message_list = driver.find_elements(By.CSS_SELECTOR, 'yt-live-chat-text-message-renderer')
    for message in message_list:
        # Get the ID of the message
        message_id = message.get_attribute('id')
        # Check if the message has already been processed
        if message_id not in processed_ids:
            # The timestamps don't work when you reload the script, they only then show the current time, not when the message was sent
            timestamp = datetime.now().strftime("%H:%M:%S")
            # Find username
            username = message.find_element(By.CSS_SELECTOR, '#author-name').text
            if username == "":
                a += 1
                break
            # Find message
            try:
                # Try to find the text of the message
                msg_elem = message.find_element(By.CSS_SELECTOR, '#message #message-text yt-formatted-string')
                msg = msg_elem.text
                # Find all emotes in the message
                emotes = message.find_elements(By.CSS_SELECTOR, '#message img')
                # Loop through all the emotes in reverse order
                for emote in emotes[::-1]:
                    alt_text = emote.get_attribute('alt')
                    # Find the index of the emote in the original message text
                    emote_index = msg_elem.get_attribute('innerHTML').index(emote.get_attribute('outerHTML'))
                    # Insert the emote at its original position in the message text
                    msg = msg[:emote_index] + ':' + alt_text + ':' + msg[emote_index:]
            except:
                # If the text is not found, use the HTML of the message
                html = message.find_element(By.CSS_SELECTOR, '#message').get_attribute('innerHTML')
                msg = re.sub('<[^<]+?>', '', html)
                # Find all emotes in the message
                emotes = message.find_elements(By.CSS_SELECTOR, '#message img')
                # Loop through all the emotes in reverse order
                for emote in emotes[::-1]:
                    alt_text = emote.get_attribute('alt')
                    # Find the index of the emote in the original message text
                    emote_index = html.index(emote.get_attribute('outerHTML'))
                    # Insert the emote at its original position in the message text
                    msg = msg[:emote_index] + ':' + alt_text + ':' + msg[emote_index:]
            # Name substitutions
            if username == "aqib mohammad":
                username = "aqua"
            elif username == "Geome-TRY Ru Dasher?":
                username = "Geometry"
            
            if any(word in msg.lower() for word in blocked_words):
                # If the message contains a blocked word, skip it
                msg = "<filtered>"
                
            if msg in commands:
                print("this is a command")
                        
            if msg == "You should go to sleep":
                print("I won't go to sleep")
            
            if a > 0:
                print(a)
            
            # Print the extracted data
            print(timestamp,":",username,":",msg)

            a = 0

            # Add the message ID to the set of processed messages
            processed_ids.add(message_id)

    gc.collect()

# Close the browser
driver.quit()