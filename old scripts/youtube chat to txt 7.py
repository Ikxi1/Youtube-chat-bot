from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import re
import time
import gc
import os

missed_name = 0
raid = 0

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.youtube.com/live_chat?v=cqUc-13tj_8")

message_list = driver.find_elements(By.CSS_SELECTOR, 'yt-live-chat-text-message-renderer')

# Read all chat messages
if not os.path.exists("chat_messages.txt"):
    open("chat_messages.txt", "w").close()
    print("Created chat_messages.txt")

with open('chat_messages.txt', 'r', encoding='utf-8') as f:
    chat_messages = set(line.strip() for line in f)
    sorted_chat_messages = sorted(chat_messages)
    for i in sorted_chat_messages:
        print(i)

# Read all message IDs
if not os.path.exists("message_ids.txt"):
    open("message_ids.txt", "w").close()
    print("Created message_ids.txt")

with open('message_ids.txt', 'r') as f:
    message_ids = set(line.strip() for line in f.readlines())

# Read all raid_ids
if not os.path.exists("raid_ids.txt"):
    open("raid_ids.txt", "w").close()
    print("Created raid_ids.txt")

with open('raid_ids.txt', 'r') as f:
    raid_ids = set(line.strip() for line in f.readlines())

# Read all blocked words
if not os.path.exists("blocked_words.txt"):
    open("blocked_words.txt", "w").close()
    print("Created blocked_words.txt\nConsider adding words you want to block to the file\nWrite one blocked term per line")

with open('blocked_words.txt', 'r') as f:
    blocked_words = [line.strip() for line in f]
    
# Read all commands
if not os.path.exists("commands.txt"):
    open("commands.txt", "w").close()
    print("Created commands.txt\nConsider adding commands to the file\nCommands start with a ! and the output is after a µ")

with open("commands.txt", "r") as f:
    commands = {}
    for line in f:
        parts = line.strip().split(";")
        command = parts[0]
        text = parts[1] if len(parts) > 1 else ""
        commands[command] = text


while True:
    # Get the latest list of messages
    message_list = driver.find_elements(By.CSS_SELECTOR, 'yt-live-chat-text-message-renderer')
    for message in message_list:
        # Get the ID of the current message
        # Just 1 ID, not a set of IDs
        # Just a string
        message_id = message.get_attribute('id')
        # Check if the message has already been processed
        if message_id not in message_ids:
            # The timestamps don't work when you reload the script, they only then show the current time, not when the message was sent
            timestamp = datetime.now().strftime("%H:%M:%S")
            # Find username
            username = message.find_element(By.CSS_SELECTOR, '#author-name').text
            if username == "":
                missed_name += 1
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
            
            if "raid" in msg and message_id not in raid_ids:
                raid += 1
                raid_ids.add(message_id)
                with open('raid_ids.txt', 'w') as f:
                    f.write('\n'.join(raid_ids))
            
            full_message = timestamp + ' : ' + username + ' : ' + msg
            # Print the message
            print(full_message)
            
            if missed_name > 0:
                print("Missed a name:", missed_name, "times.")

            chat_messages.add(full_message)
            with open('chat_messages.txt', 'w', encoding='utf-8') as f:
                for message in sorted(chat_messages):
                    f.write(message + '\n')
            
            # Print if a raid is happening
            if raid >= 5:
                print("THERE IS A RAID HAPPENING!!!")
                raid = 0

            # Print if someone tells me to sleep
            if "you should go to sleep" in msg or "You should go to sleep" in msg:
                print("I won't go to sleep")
            
            missed_name = 0

            # Add the message ID to the set of processed messages
            message_ids.add(message_id)
            with open('message_ids.txt', 'w') as f:
                f.write('\n'.join(message_ids))

    gc.collect()

# Close the browser
driver.quit()