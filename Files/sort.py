import os
import base64
import requests

# Constants
PROTOCOLS = ['vmess', 'vless', 'trojan', 'ss', 'ssr']
BASE_URL = "https://raw.githubusercontent.com/MRT-project/v2ray-configs/main/All_Configs_Sub.txt"
OUTPUT_DIR = os.path.abspath(os.path.join(os.getcwd(), '..', 'Splitted-By-Protocol'))

def init_output_files():
    """Create/clear output files for each protocol."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for protocol in PROTOCOLS:
        with open(os.path.join(OUTPUT_DIR, f"{protocol}.txt"), "w") as f:
            pass  # Clear file

def fetch_configs():
    """Fetch the raw text config from GitHub."""
    response = requests.get(BASE_URL)
    response.raise_for_status()  # Raise error on failed request
    return response.text.splitlines()

def process_configs(config_lines):
    """Categorize configs by protocol."""
    categorized = {protocol: [] for protocol in PROTOCOLS}
    for config in config_lines:
        for protocol in PROTOCOLS:
            if config.startswith(protocol):
                if protocol == 'vmess':
                    # Write vmess line directly to file
                    with open(os.path.join(OUTPUT_DIR, f"{protocol}.txt"), "a") as f:
                        f.write(config + '\n')
                else:
                    categorized[protocol].append(config)
                break
    return categorized

def save_encoded_configs(categorized_configs):
    """Base64 encode and save the configs for each protocol (except vmess)."""
    for protocol, lines in categorized_configs.items():
        if protocol == 'vmess':
            continue  # Already written directly
        encoded = base64.b64encode('\n'.join(lines).encode('utf-8')).decode('utf-8')
        with open(os.path.join(OUTPUT_DIR, f"{protocol}.txt"), "w") as f:
            f.write(encoded)

def main():
    init_output_files()
    config_lines = fetch_configs()
    categorized_configs = process_configs(config_lines)
    save_encoded_configs(categorized_configs)

if __name__ == "__main__":
    main()
