import os
import base64
import binascii
import pybase64
from pyrogram import Client

# --- KONFIGURASI ---
API_ID = 12345678
API_HASH = "your_api_hash"
SESSION_STRING = "your_session_pyrogram_string"

# --- KONSTANTA ---
PROTOCOLS = ["vmess", "vless", "trojan", "ss", "ssr", "hy2", "tuic", "warp://"]
FIXED_TEXT_TEMPLATE = """"""
DEFAULT_FIXED_TEXT = """"""

def filter_protocols(data: list[str], protocols: list[str]) -> list[str]:
    return [line for line in data if any(proto in line for proto in protocols)]

def ensure_directories() -> tuple[str, str]:
    root = os.path.abspath(os.path.join(os.getcwd(), ".."))
    base64_dir = os.path.join(root, "Base64")
    os.makedirs(root, exist_ok=True)
    os.makedirs(base64_dir, exist_ok=True)
    return root, base64_dir

def clean_existing_files(output_folder: str, base64_folder: str):
    def safe_remove(path):
        if os.path.exists(path):
            os.remove(path)
    safe_remove(os.path.join(output_folder, "All_Configs_Sub.txt"))
    for i in range(20):
        safe_remove(os.path.join(output_folder, f"Sub{i}.txt"))
        safe_remove(os.path.join(base64_folder, f"Sub{i}_base64.txt"))

def write_combined_configs(filepath: str, configs: list[str]):
    with open(filepath, "w") as f:
        f.write(DEFAULT_FIXED_TEXT)
        for config in configs:
            f.write(config.strip() + "\n")

def split_and_encode_configs(source_path: str, output_dir: str, base64_dir: str, max_lines: int = 500):
    with open(source_path, "r") as f:
        lines = f.readlines()

    total = len(lines)
    chunks = (total + max_lines - 1) // max_lines

    for i in range(chunks):
        start = i * max_lines
        end = min((i + 1) * max_lines, total)
        profile_title = f"🆓 Telegram Config | Sub{i + 1} 🔥"
        encoded_title = base64.b64encode(profile_title.encode()).decode()
        header = FIXED_TEXT_TEMPLATE.format(encoded_title=encoded_title)

        chunk_file = os.path.join(output_dir, f"Sub{i + 1}.txt")
        with open(chunk_file, "w") as f:
            f.write(header)
            f.writelines(lines[start:end])

        with open(chunk_file, "r") as f:
            encoded_data = base64.b64encode(f.read().encode()).decode()

        with open(os.path.join(base64_dir, f"Sub{i + 1}_base64.txt"), "w") as f:
            f.write(encoded_data)

def fetch_telegram_messages(channels: list[str], limit: int = 50) -> list[str]:
    messages = []
    with Client(name="session", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH) as app:
        for channel in channels:
            for message in app.get_chat_history(channel, limit=limit):
                if message.text:
                    messages.append(message.text)
    return messages

def main():
    output_dir, base64_dir = ensure_directories()
    clean_existing_files(output_dir, base64_dir)

    telegram_channels = ["heyatserver", "V2rayNG_vnp", "XRayConfigs"]
    telegram_messages = fetch_telegram_messages(telegram_channels, limit=100)
    telegram_filtered = filter_protocols(telegram_messages, PROTOCOLS)

    all_configs_path = os.path.join(output_dir, "All_Configs_Sub.txt")
    write_combined_configs(all_configs_path, telegram_filtered)
    split_and_encode_configs(all_configs_path, output_dir, base64_dir)

if __name__ == "__main__":
    main()
