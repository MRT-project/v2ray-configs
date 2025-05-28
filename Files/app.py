import os
import base64
import requests
import binascii
import pybase64

TIMEOUT = 20  # seconds

FIXED_TEXT_TEMPLATE = """#profile-title: base64:{encoded_title}
#profile-update-interval: 1
#subscription-userinfo: upload=29; download=12; total=10737418240000000; expire=2546249531
#support-url: https://github.com/MRT-project/v2ray-configs
#profile-web-page-url: https://github.com/MRT-project/v2ray-configs
"""

DEFAULT_FIXED_TEXT = """#profile-title: base64:8J+GkyBHaXRodWIgfCBCYXJyeS1mYXIg8J+ltw==
#profile-update-interval: 1
#subscription-userinfo: upload=29; download=12; total=10737418240000000; expire=2546249531
#support-url: https://github.com/MRT-project/v2ray-configs
#profile-web-page-url: https://github.com/MRT-project/v2ray-configs
"""

PROTOCOLS = ["vmess", "vless", "trojan", "ss", "ssr", "hy2", "tuic", "warp://"]


def decode_base64(encoded: bytes) -> str:
    """Decode base64 with fallback encodings."""
    for encoding in ["utf-8", "iso-8859-1"]:
        try:
            padded = encoded + b"=" * (-len(encoded) % 4)
            return pybase64.b64decode(padded).decode(encoding)
        except (UnicodeDecodeError, binascii.Error):
            continue
    return ""


def fetch_and_decode_links(links: list[str], decode_func) -> list[str]:
    """Fetch content from links and decode using a specified function."""
    decoded_results = []
    for link in links:
        try:
            response = requests.get(link, timeout=TIMEOUT)
            decoded = decode_func(response.content)  # Always pass bytes
            if decoded:
                decoded_results.append(decoded)
        except requests.RequestException:
            continue
    return decoded_results


def filter_protocols(data: list[str], protocols: list[str]) -> list[str]:
    """Filter data lines that contain any of the specified protocols."""
    return [line for line in data if any(proto in line for proto in protocols)]


def ensure_directories() -> tuple[str, str]:
    """Create output and Base64 directories if they don't exist."""
    root = os.path.abspath(os.path.join(os.getcwd(), ".."))
    base64_dir = os.path.join(root, "Base64")
    os.makedirs(root, exist_ok=True)
    os.makedirs(base64_dir, exist_ok=True)
    return root, base64_dir


def clean_existing_files(output_folder: str, base64_folder: str):
    """Delete previously generated files to avoid duplicates."""
    def safe_remove(path):
        if os.path.exists(path):
            os.remove(path)

    safe_remove(os.path.join(output_folder, "All_Configs_Sub.txt"))
    safe_remove(os.path.join(output_folder, "All_Configs_base64_Sub.txt"))

    for i in range(20):
        safe_remove(os.path.join(output_folder, f"Sub{i}.txt"))
        safe_remove(os.path.join(base64_folder, f"Sub{i}_base64.txt"))


def write_combined_configs(filepath: str, configs: list[str]):
    """Write fixed header and merged configs into a single file."""
    with open(filepath, "w") as f:
        f.write(DEFAULT_FIXED_TEXT)
        for config in configs:
            f.write(config.strip() + "\n")


def split_and_encode_configs(source_path: str, output_dir: str, base64_dir: str, max_lines: int = 500):
    """Split large config file into smaller ones and write base64 versions."""
    with open(source_path, "r") as f:
        lines = f.readlines()

    total = len(lines)
    chunks = (total + max_lines - 1) // max_lines

    for i in range(chunks):
        start = i * max_lines
        end = min((i + 1) * max_lines, total)
        profile_title = f"🆓 Git:MRT-project | Sub{i + 1} 🔥"
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


def main():
    output_dir, base64_dir = ensure_directories()
    clean_existing_files(output_dir, base64_dir)

    base64_links = [
        "https://raw.githubusercontent.com/MrPooyaX/VpnsFucking/main/BeVpn.txt",
        "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/xray/base64/mix",
        "https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/sub.txt",
        "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/reality",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vmess",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/trojan",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/shadowsocks",
        "https://raw.githubusercontent.com/ts-sf/fly/main/v2",
        "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
        "https://mrpooya.top/SuperApi/BE.php",
        "https://raw.githubusercontent.com/MrPooyaX/VpnsFucking/main/BeVpn.txt"
    ]

    dir_links = [
        "https://raw.githubusercontent.com/IranianCypherpunks/sub/main/config",
        "https://raw.githubusercontent.com/sashalsk/V2Ray/main/V2Config",
        "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity.txt",
        "https://raw.githubusercontent.com/itsyebekhe/HiN-VPN/main/subscription/normal/mix",
        "https://raw.githubusercontent.com/sarinaesmailzadeh/V2Hub/main/merged",
        "https://raw.githubusercontent.com/freev2rayconfig/V2RAY_SUBSCRIPTION_LINK/main/v2rayconfigs.txt",
        "https://raw.githubusercontent.com/Everyday-VPN/Everyday-VPN/main/subscription/main.txt",
        "https://raw.githubusercontent.com/C4ssif3r/V2ray-sub/main/all.txt",
        "https://mrpooya.top/SuperApi/V7pRO.php"
    ]

    decoded_base64 = fetch_and_decode_links(base64_links, decode_base64)
    decoded_dirs = fetch_and_decode_links(dir_links, lambda x: x.decode("utf-8", errors="ignore"))

    combined = decoded_base64 + decoded_dirs
    merged = filter_protocols(combined, PROTOCOLS)

    all_configs_path = os.path.join(output_dir, "All_Configs_Sub.txt")
    write_combined_configs(all_configs_path, merged)

    split_and_encode_configs(all_configs_path, output_dir, base64_dir)


if __name__ == "__main__":
    main()
