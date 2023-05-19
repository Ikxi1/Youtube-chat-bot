from datetime import datetime
import os

# Test variable to not interfere with normal usage
test = False
if test:
	test_file = '_test'
else:
	test_file = ''


class Files:
	def __init__(self):
		# Get today's date to add to file names
		today = datetime.now().strftime("%Y-%m-%d")

		# Create data folder, if none exists
		dir_data = "data" + test_file + "/"
		if not os.path.exists(dir_data):
			os.mkdir(dir_data)
			print("Created data/ folder\nAll files will be written here")


		# Create chat messages folder, if none exists
		dir_chat_messages = dir_data + "chat_messages/"
		if not os.path.exists(dir_chat_messages):
			os.mkdir(dir_chat_messages)
			print("Created chat_messages/ folder\nAll chat messages will be saved here")

		# Create chat messages file of the current day, if none exists
		self.file_chat_messages = dir_chat_messages + "chat_messages" + "_" + today + ".txt"
		if not os.path.exists(self.file_chat_messages):
			open(self.file_chat_messages, "w", encoding='utf-8').close()
			print(
				"Created " +
				self.file_chat_messages +
				"\nAll messages from " +
				today +
				" will be saved here"
			)

		# Read all chat messages from file and write them
		with open(self.file_chat_messages, 'r', encoding='utf-8') as f:
			self.chat_messages = set(line.strip() for line in f)
			sorted_chat_messages = sorted(self.chat_messages)


		# Create message ids folder, if none exists
		dir_message_ids = dir_data + "message_ids/"
		if not os.path.exists(dir_message_ids):
			os.mkdir(dir_message_ids)
			print("Created message_ids/ folder\nAll chat messages will be saved here")

		# Create message ids file, if none exists
		self.file_message_ids = dir_message_ids + "message_ids-" + "_" + today + ".txt"
		if not os.path.exists(self.file_message_ids):
			open(self.file_message_ids, "w").close()
			print(
				"Created " +
				self.file_message_ids +
				"\nAll message IDs from "
			)

		# Read all message IDs from file
		with open(self.file_message_ids, 'r') as f:
			self.message_ids = set(line.strip() for line in f.readlines())


		# Create raid ids folder, if none exists
		dir_raid_ids = dir_data + "raid_ids/"
		if not os.path.exists(dir_raid_ids):
			os.mkdir(dir_raid_ids)
			print(
				"Created raid_ids/ folder"
			)

		# Create raid ids file, if none exists
		self.file_raid_ids = dir_raid_ids + "raid_ids" + "_" + today + ".txt"
		if not os.path.exists(self.file_raid_ids):
			open(self.file_raid_ids, "w").close()
			print("Created " + self.file_raid_ids)

		# Read all raid_ids from file
		with open(self.file_raid_ids, 'r') as f:
			self.raid_ids = set(line.strip() for line in f.readlines())


		# Create blocked words file, if none exists
		self.file_blocked_words = dir_data + "blocked_words.txt"
		if not os.path.exists(self.file_blocked_words):
			open(self.file_blocked_words, "w").close()
			print(
				"Created blocked_words.txt\n"
				"Consider adding words you want to block to the file\n"
				"Write one blocked term/sentence per line"
			)

		# Read all blocked words from file
		with open(self.file_blocked_words, 'r') as f:
			self.blocked_words = [line.strip() for line in f]


		# Create commands file, if none exists
		self.file_commands = dir_data + "commands.txt"
		if not os.path.exists(self.file_commands):
			open(self.file_commands, "w", encoding='utf-8').close()
			print(
				"Created commands file\n"
				"Consider adding commands to the file\n"
				"Commands start with a ! and the output is after a ;"
			)

		# Read all commands from file
		with open(self.file_commands, "r", encoding='utf-8') as f:
			self.commands = {}
			for line in f:
				# Split the lines at µ
				parts = line.strip().split("µ")
				# Part 1 of the line becomes command
				command = parts[0]
				# Part 2 of the line becomes output text
				# Check if there are any characters
				text = parts[1] if len(parts) > 1 else ""
				self.commands[command] = text

		# Read name exchange list
		self.file_name_exchanges = dir_data + "name_exchanges.txt"
		if not os.path.exists(self.file_name_exchanges):
			open(self.file_name_exchanges, "w", encoding='utf-8').close()
			print(
				"Created name exchange file\n"
				"Consider adding names of people here that you want to replace with a nickname"
			)

		with open(self.file_name_exchanges, "r", encoding='utf-8') as f:
			self.exchange_names = {}
			for line in f:
				parts = line.strip().split("µ")
				original_name = parts[0]
				replaced_name = parts[1] if len(parts) > 1 else ""
				self.exchange_names[original_name] = replaced_name

	def write_messages(self, chat_message):
		# Method for writing chat messages back to file
		self.chat_messages.add(chat_message)
		with open(self.file_chat_messages, 'w', encoding='utf-8') as f:
			for message in sorted(self.chat_messages):
				f.write(message + '\n')

	def write_message_ids(self, msg_id):
		# Method for writing message IDs back to file
		self.message_ids.add(msg_id)
		with open(self.file_message_ids, 'w') as f:
			f.write('\n'.join(self.message_ids))

	def write_raid_ids(self, raid_id):
		# Method for writing raid IDs back to the file
		self.raid_ids.add(raid_id)
		with open(self.file_raid_ids, 'w') as f:
			f.write('\n'.join(self.raid_ids))
