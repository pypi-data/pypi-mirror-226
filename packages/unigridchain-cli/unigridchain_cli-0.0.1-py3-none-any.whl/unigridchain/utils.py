import hashlib
import os
import requests
from rich import print
from rich.progress import Progress
import subprocess
import re
import json
from .config import (_hedgehog_repo, _hedgehog_path, _unigridchain_repo,
                     _base_unigridchain_name, _GENESIS_URL, _GENESIS_CHECKSUM, _daemons_path)
import socket
import random

CONFIG_FILE = 'ugd_config.json'
base_path_chain = os.path.expanduser("~/.cosmos-daemon/config")
GENESIS_PATH = os.path.join(base_path_chain, "genesis.json")
DEFAULT_CONFIG_PATH = os.path.join(base_path_chain, 'ugd_config.json')
CONFIG_ENV_VAR = 'UNIGRID_CONFIG_PATH'


def download_and_install(repo_url):
    """Download and install the latest release from the given repo_url."""
    print(f"Downloading and installing {repo_url}...")
    # Extract owner and repo from the repo_url
    parts = repo_url.split("/")
    owner = parts[-2]
    repo = parts[-1]

    # Fetch the latest release information
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    print(f"Fetching release information from {api_url}...")
    response = requests.get(api_url)
    data = response.json()

    # Extract the version number
    version = data["tag_name"]
    print(f"Latest version: {version}")

    # If the version starts with "v", remove it
    if version.startswith("v"):
        version = version[1:]

    # Construct the desired filenames
    hedgehog_filename = f"hedgehog-{version}-x86_64-linux-gnu.bin"
    cosmos_filename = f"cosmos-daemond-v{version}-linux-amd64"

    # Search for the asset with the desired filename
    download_url = None
    for asset in data["assets"]:
        if asset["name"] == hedgehog_filename or asset["name"] == cosmos_filename:
            download_url = asset["browser_download_url"]
            break

    if not download_url:
        print(f"ERROR: Could not find asset with desired filename")
        return

    # Load the configuration
    config = load_configuration()
    if not config:
        print("Error: Could not load configuration.")
        return
    hedgehog_path = config.get('hedgehog_path', _daemons_path)
    unigridchain_path = config.get('unigridchain_path')

    hedgehog_download_url = None
    cosmos_download_url = None
    for asset in data["assets"]:
        if asset["name"] == hedgehog_filename:
            hedgehog_download_url = asset["browser_download_url"]
        elif asset["name"] == cosmos_filename:
            cosmos_download_url = asset["browser_download_url"]

    if hedgehog_download_url:
        download_and_move(hedgehog_download_url,
                          hedgehog_filename, hedgehog_path)
    else:
        print(f"ERROR: Could not find hedgehog asset with desired filename")

    if cosmos_download_url:
        # destination_path = os.path.join(unigridchain_path, cosmos_filename)
        download_and_move(cosmos_download_url,
                          cosmos_filename, unigridchain_path)
        print(f"Setting execute permissions for {unigridchain_path}")
        os.chmod(unigridchain_path, 0o755)  # This sets the execute permission
    else:
        print(f"ERROR: Could not find cosmos asset with desired filename")


def download_and_move(download_url, filename, destination_path):
    """Helper function to download and move the asset."""
    # Download the release asset with progress
    response = requests.get(download_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    temp_filename = os.path.join("/tmp", filename)
    print(f"Downloading {temp_filename}...")

    # Download the release asset with rich progress bar
    with Progress() as progress:
        task = progress.add_task("[cyan]Downloading...", total=total_size)
        with open(temp_filename, 'wb') as file:
            for data in response.iter_content(1024):
                file.write(data)
                progress.update(task, advance=len(data))

    # Ensure that the entire file has been downloaded
    if total_size != 0 and os.path.getsize(temp_filename) != total_size:
        print("ERROR: Something went wrong while downloading the file.")
    else:
        print(f"Downloaded {temp_filename}")
        # shutil.move(temp_filename, destination_path)
        move_with_sudo_and_set_permissions(temp_filename, destination_path)
        print(f"[green]Moved {temp_filename} to {destination_path}[/green]")


def move_with_sudo_and_set_permissions(src, dest):
    """Move a file using sudo and set executable permissions."""
    move_cmd = ["sudo", "mv", src, dest]
    chmod_cmd = ["sudo", "chmod", "+x", dest]
    try:
        subprocess.check_call(move_cmd)
        subprocess.check_call(chmod_cmd)
    except subprocess.CalledProcessError:
        print("Failed to move the file or set permissions with elevated permissions.")
        return False
    return True


def update_hedgehog():
    """Update the hedgehog daemon."""
    hedgehog_ver = get_version()
    print(f"[green]Installed Hedgehog version: {hedgehog_ver}[/green]")
    github_version = get_github_version(_hedgehog_repo)
    print(f"[yellow]Latest Hedgehog version: {github_version}[/yellow]")
    if hedgehog_ver and github_version and hedgehog_ver < github_version:
        print(f"New version {github_version} available. Updating...")
        if is_hedgehog_running():
            stop_hedgehog_daemon()
        download_and_install(_hedgehog_repo)
    else:
        print("[green]You have the latest hedgehog installed![/green]")


def update_unigridchain():
    """Update the unigridchain daemon."""
    # Load the configuration
    config = load_configuration()
    if not config:
        print("Error: Could not load configuration.")
        return
    if config:
        base_path = config.get('base_path')
        unigridchain_path = config.get(
            'unigridchain_path', '/usr/local/bin/cosmos-daemond-v0.0.1-linux-amd64')

    chain_ver = get_latest_installed_version(base_path, _base_unigridchain_name)
    print(f"[green]Installed Unigridchain version: {chain_ver}[/green]")
    github_version_chain = get_github_version(_unigridchain_repo)
    print(
        f"[yellow]Latest Unigridchain version: {github_version_chain}[/yellow]")

    # If unigridchain is not installed
    if chain_ver is None:
        print(
            f"Unigridchain is not installed. Installing version {github_version_chain}...")
        download_and_install(_unigridchain_repo)
    # If unigridchain is installed but not up-to-date
    elif chain_ver and github_version_chain and chain_ver < github_version_chain:

        print(f"New version {github_version_chain} available. Updating...")
        if is_unigridchain_running(unigridchain_path):
            stop_unigridchain_daemon()
        old_file_path = unigridchain_path
        if os.path.exists(old_file_path):
            os.remove(old_file_path)
            print(f"[red]Removed old version at {old_file_path}[/red]")
        download_and_install(_unigridchain_repo)
    else:
        print("[green]You have the latest unigridchain installed![/green]")


def start_daemon(daemon_name):
    # Logic to start the specified daemon
    pass


def get_status():
    # Define the command to be executed
    # Load the configuration
    config = load_configuration()
    if not config:
        print("Error: Could not load configuration.")
        return
    hedgehog_path = config.get('hedgehog_path', _hedgehog_path)
    print(f"Checking status of {hedgehog_path}...")
    cmd = [hedgehog_path, "cli", "--version"]
    # Execute the command and capture the output
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Print the output
    print(result.stdout)
    return "Running"  # Example status

def get_version():
    # Get the version number of the installed daemon
    # Execute the command and capture the output
    result = call_hedgehog_cli(["--version"])
    # Extract the version number using a regular expression
    version_pattern = r"(\d+\.\d+\.\d+)"
    match = re.search(version_pattern, result.stdout)
    if match:
        version = match.group(1)
        # print(version)
        # return "0.0.6"
        return version
    else:
        print("Version number not found!")
        return None


def update_daemon(repo_url):
    # Logic to update the daemon to the latest release from the given repo_url
    pass


def update_if_needed():
    local_version = get_version()
    github_version = get_github_version(_hedgehog_repo)

    # Compare the local version with the GitHub version
    if local_version and github_version and local_version < github_version:
        print(f"New version {github_version} available. Updating...")
        download_and_install(
            _hedgehog_repo)
    else:
        print("You have the latest version installed!")


def get_github_version(repo_url):
    # Extract owner and repo from the repo_url
    parts = repo_url.split("/")
    owner = parts[-2]
    repo = parts[-1]

    # Fetch the latest release information from GitHub
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(api_url)
    data = response.json()

    # Extract the version number from the "tag_name" field and remove the "v" prefix
    version_pattern = r"v(\d+\.\d+\.\d+)"
    match = re.search(version_pattern, data["tag_name"])
    if match:
        return match.group(1)
    else:
        print("Version number not found on GitHub!")
        return None


def is_hedgehog_running():
    # Check if the hedgehog daemon is running
    result = call_hedgehog_cli(["gridspork-list"])

    # Check if the output contains the "Connection refused" error
    if "Connection refused" in result.stderr:
        return False

    # Try to parse the output as JSON to see if it's a valid response
    try:
        json.loads(result.stdout)
        return True
    except json.JSONDecodeError:
        return False


def stop_hedgehog_daemon():
    """Stop the hedgehog daemon without invoking the CLI command."""
    config = load_configuration()
    if not config:
        print("Error: Could not load configuration.")
        return
    hedgehog_path = config.get('hedgehog_path', _hedgehog_path)
    if os.path.exists(hedgehog_path):
        # Stop the hedgehog daemon
        call_hedgehog_cli(["stop"])
        print("[green]Stopped the hedgehog daemon[/green]")
    else:
        print(
            f"[red]Hedgehog daemon not found at {hedgehog_path}. Please run 'unigridchain-cli setup' to install it.[/red]")


def stop_unigridchain_daemon():
    try:
        # Get the PID of the unigridchain daemon
        result = subprocess.run(
            ['pgrep', '-f', 'cosmos-daemond'], capture_output=True, text=True)
        pid = result.stdout.strip()

        if pid:
            # Send a termination signal to the process
            subprocess.run(['kill', pid])
            print("[green]Unigridchain daemon stopped successfully[/green]")
        else:
            print("[red]Unigridchain daemon is not running[/red]")
    except Exception as e:
        print(f"[red]Error stopping Unigridchain daemon: {e}[/red]")


def call_hedgehog_cli(args):
    config = load_configuration()
    if not config:
        print("Error: Could not load configuration.")
        return
    hedgehog_path = config.get('hedgehog_path', _hedgehog_path)
    cmd = [hedgehog_path, "cli"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result


def is_daemon_installed():
    config = load_configuration()
    if not config:
        print("Error: Could not load configuration.")
        return
    hedgehog_path = config.get('hedgehog_path', _hedgehog_path)
    return os.path.exists(hedgehog_path)


def get_latest_installed_version(directory, daemon_prefix):
    """Get the latest installed version of the daemon from the given directory."""
    # Regex pattern to match filenames with version numbers and specific prefix
    pattern = re.compile(rf'{daemon_prefix}-v(\d+\.\d+\.\d+)')

    # List all files in the directory
    files = os.listdir(directory)

    # Filter files that match our pattern
    version_files = [f for f in files if pattern.search(f)]

    # If no matching files, return None
    if not version_files:
        return None

    # Extract version numbers from the filenames
    versions = [pattern.search(f).group(1) for f in version_files]

    # Return the latest version
    return max(versions, key=lambda v: tuple(map(int, v.split('.'))))


def get_unigridchain_fullpath(base_path, prefix=_base_unigridchain_name):
    """Get the full path of the installed unigridchain from the given directory."""
    # List all files in the base_path directory
    files = os.listdir(base_path)

    # Filter files that start with the given prefix
    matching_files = [f for f in files if f.startswith(prefix)]

    # Return the full path of the first matching file or None if no match is found
    return os.path.join(base_path, matching_files[0]) if matching_files else None


def is_unigridchain_running(path):
    """Check if the unigridchain daemon is running."""
    unigridchain_path = path
    if not unigridchain_path:
        print("[red]Unigridchain daemon not found![/red]")
        return False

    # print(f"Checking if Unigridchain daemon is running at {unigridchain_path}...")
    cmd = [unigridchain_path, "status"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        # Parse the JSON output
        output = json.loads(result.stdout)
        # Check for the presence of the "NodeInfo" key
        if "NodeInfo" in output:
            return True
        return False
    except FileNotFoundError:
        return False
    except json.JSONDecodeError:
        # print("[magenta]Unigridchain daemon is not currently running[/magenta]")
        return False
    except Exception as e:
        print(f"[red]Error checking Unigridchain daemon status: {e}[/red]")
        return False


def is_version_up_to_date():
    local_version = get_version()
    github_version = get_github_version(_hedgehog_repo)
    return local_version == github_version


def fetch_and_create_genesis():
    """Fetch the genesis.json from GitHub and save it to the specified path."""
    response = requests.get(_GENESIS_URL)

    # Check if the request was successful
    if response.status_code == 200:
        with open(GENESIS_PATH, 'w') as file:
            file.write(response.text)
        print("[green]Successfully fetched and created genesis.json![/green]")
    else:
        print(
            f"[red]Failed to fetch genesis.json. HTTP Status Code: {response.status_code}[/red]")


def check_and_create_genesis():
    """Check if genesis.json exists, if not, fetch and create it."""

    # Check if the directory exists
    if not os.path.exists(base_path_chain):
        print("[yellow]Directory for genesis.json not found. Creating it...[/yellow]")
        os.makedirs(base_path_chain)

    # Now check for the genesis.json file
    if not os.path.exists(GENESIS_PATH):
        print("[yellow]genesis.json not found. Fetching from GitHub...[/yellow]")
        fetch_and_create_genesis()

        # Compute the SHA256 checksum of the downloaded file
        computed_checksum = compute_sha256(GENESIS_PATH)
        # Replace with the expected checksum
        expected_checksum = _GENESIS_CHECKSUM
        print(f"Expected genesis.json SHA256: {expected_checksum}")
        print(f"Downloaded genesis.json SHA256: {computed_checksum}")
        if computed_checksum == expected_checksum:
            print("Checksum matches. File is intact.")
        else:
            print(
                "[red]Checksum does not match. File might be corrupted or tampered with.[/red]")
            # Handle the mismatch, e.g., by deleting the file or notifying the user
    else:
        print("genesis.json already exists. Skipping...")


def compute_sha256(file_path):
    """Compute the SHA256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_java_version():
    try:
        # Run the 'java -version' command
        result = subprocess.run(['java', '-version'],
                                stderr=subprocess.PIPE, text=True)
        output = result.stderr

        # Extract the version number from the output
        match = re.search(r'version "([\d]+)', output)
        if match:
            return int(match.group(1))
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def install_java_17():
    try:
        # Update the package list
        subprocess.run(['sudo', 'apt', 'update'])

        # Install OpenJDK 17
        subprocess.run(['sudo', 'apt', 'install', '-y', 'openjdk-17-jdk'])
    except Exception as e:
        print(f"Error: {e}")


def is_port_available(port):
    """Check if a port is available."""
    print(f"Checking if port {port} is available...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.bind(("0.0.0.0", port))
            return True
        except OSError:
            return False


def get_random_available_port():
    """Get a random available port between 1024 and 65535."""
    port = random.randint(1024, 65535)
    while not is_port_available(port):
        port = random.randint(1024, 65535)
    return port


def enable_udp_port(port):
    """Enable a port for UDP using ufw."""
    if not ensure_ufw_installed():
        print("ufw is not installed. Please install ufw to manage firewall rules.")
        return

    # Open the port in ufw
    try:
        subprocess.run(['sudo', 'ufw', 'allow', str(port)+'/udp'], check=True)
        print(f"Port {port} enabled for UDP in ufw.")
    except subprocess.CalledProcessError:
        print(f"Failed to enable port {port} for UDP in ufw.")


def enable_tcp_port(port):
    """Enable a port for TCP using ufw."""
    if not ensure_ufw_installed():
        print("ufw is not installed. Please install ufw to manage firewall rules.")
        return

    # Open the port in ufw
    try:
        subprocess.run(['sudo', 'ufw', 'allow', str(port)+'/tcp'], check=True)
        print(f"Port {port} enabled for TCP in ufw.")
    except subprocess.CalledProcessError:
        print(f"Failed to enable port {port} for TCP in ufw.")


def ensure_ufw_installed():
    """Ensure ufw is installed. If not, install it."""
    try:
        subprocess.run(['which', 'ufw'], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=True)
        print("ufw is already installed, skipping...")
        return True
    except subprocess.CalledProcessError:
        print("ufw is not installed. Installing...")
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=True)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'ufw'], check=True)
            print("ufw installed successfully.")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install ufw. Please install it manually.")
            return False


def save_config(**kwargs):
    config_path = os.environ.get(CONFIG_ENV_VAR, None)
    if not config_path:
        config_path = set_config_path_env_var()

    # Save the configuration to the specified path
    with open(config_path, 'w') as f:
        json.dump(kwargs, f, indent=4)

    # Update ~/.bashrc with the new config path
    update_bashrc_with_config_path(config_path)
    print(
        f"UNIGRID_CONFIG_PATH: {os.environ.get('UNIGRID_CONFIG_PATH', 'Not Set')}")


def set_config_path_env_var():
    # Ask for custom location for the configuration file
    print(
        f"[yellow]The default location of the configuration file is {base_path_chain}[/yellow]")
    choice = input(
        "Would you like to change the location? (Y/N) ").strip().lower()

    if choice == 'y':
        new_path = input(
            "Please enter the new location for the configuration file: ").strip()

        # Ensure the directory exists
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        updated_path = os.path.join(new_path, 'ugd_config.json')
        os.environ[CONFIG_ENV_VAR] = updated_path
        print(f"Environment variable {CONFIG_ENV_VAR} set to {updated_path}")
    else:
        os.environ[CONFIG_ENV_VAR] = DEFAULT_CONFIG_PATH
        print(f"Using default location: {DEFAULT_CONFIG_PATH}")
        updated_path = DEFAULT_CONFIG_PATH

    # Ensure the directory exists
    dir_path = os.path.dirname(updated_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # Create or update the ugd_config.json with the custom locations
    config = {}
    if os.path.exists(updated_path):
        with open(updated_path, "r") as f:
            config = json.load(f)

    with open(updated_path, "w") as f:
        json.dump(config, f)

    return updated_path


def update_bashrc_with_config_path(config_path):
    bashrc_path = os.path.expanduser("~/.bashrc")

    # Check if CONFIG_ENV_VAR exists in ~/.bashrc and remove it
    subprocess.run(f"sed -i '/{CONFIG_ENV_VAR}/d' {bashrc_path}", shell=True)

    # Append the new definition to ~/.bashrc
    with open(bashrc_path, 'a') as f:
        f.write(f'export {CONFIG_ENV_VAR}={config_path}\n')


def load_configuration():
    """Load and return the configuration from the file specified by $UNIGRID_CONFIG_PATH."""
    config_path = os.environ.get('UNIGRID_CONFIG_PATH')
    if not config_path or not os.path.exists(config_path):
        print("[red]Configuration file not found. Please run the setup first.[/red]")
        return None

    with open(config_path, 'r') as f:
        config = json.load(f)

    return config


def print_important_message(message, color="magenta"):
    # Remove color codes to get the actual length
    clean_message = re.sub(r'\[\w+\]', '', message)
    # 6 for the three asterisks on each side
    total_length = len(clean_message) + 6
    asterisks = '*' * total_length
    colored_asterisks = f"[{color}]{asterisks}[/{color}]"

    print(colored_asterisks)
    print(f"[{color}]*******[/{color}]{message}[{color}]*******[/{color}]")
    print(colored_asterisks)
