from .utils import (
    download_and_install,
    get_version,
    get_github_version,
    is_hedgehog_running,
    stop_hedgehog_daemon,
    check_and_create_genesis,
    install_java_17,
    get_random_available_port,
    enable_tcp_port,
    is_daemon_installed,
    get_latest_installed_version,
    is_unigridchain_running,
    stop_unigridchain_daemon,
    update_hedgehog,
    update_unigridchain,
    get_java_version,
    is_port_available,
    enable_udp_port,
    save_config,
    set_config_path_env_var,
    load_configuration,
    print_important_message,
    base_path_chain
)
from .config import (
    _hedgehog_repo,
    _unigridchain_repo,
    _HEDGEHOG_PORT,
    _UNIGRIDCHAIN__gRPC_PORT,
    _UNIGRIDCHAIN__REST_PORT,
    _UNIGRIDCHAIN__BFT_PORT,
    _daemons_path
)
import re
import click
from rich import print
import os
import requests
import subprocess
import pkg_resources

script_path = pkg_resources.resource_filename(
    'unigridchain', 'scripts/post_setup.sh')


@click.group()
def cli():
    pass


@cli.command()
def init():
    # Prompt the user for necessary parameters
    user = input("Enter the username to run the service (e.g., unigrid): ")
    working_dir = input(
        "Enter the working directory for the service (e.g., /home/<user>/.unigridchain): ")
    hedgehog_dir = input(
        "Enter the directory where hedgehog is installed (e.g., /usr/local/bin/hedgehog.bin): ")
    unigridchaind_dir = input(
        "Enter the directory where unigridchaind is installed (e.g., /usr/local/bin/unigridchaind): ")
    exec_path = "/usr/local/bin/ugd_monitor.py"
    args = input("Enter any arguments for the script (leave blank if none): ")

    # Load the template
    template = """
    [Unit]
    Description=Unigrid Monitor Service
    After=network.target

    [Service]
    Type=simple
    User={}
    WorkingDirectory={}
    ExecStart={} {}
    Restart=always
    RestartSec=5
    StandardOutput=syslog
    StandardError=syslog
    SyslogIdentifier=unigrid-monitor

    [Install]
    WantedBy=multi-user.target
    """.format(user, working_dir, exec_path, args)

    # Write the configuration to a .service file
    with open("unigrid-monitor.service", "w") as file:
        file.write(template)

    print("unigrid-monitor.service file has been generated!")


@cli.command()
def setup():
    """Download and install the latest releases for the daemons."""
    # Check which Java version is installed
    version = get_java_version()

    if version is None:
        print("Java is not installed.")
        install_java_17()
    elif version < 17:
        print(f"Java version {version} detected. Installing Java 17...")
        install_java_17()
    else:
        print(f"Java version {version} or higher is already installed.")
    # Prompt the user to change the default path of the configuration file
    config = set_config_path_env_var()
    print(f"Config: {config}")
    # Initialize the ports with their default values
    udp_port = _HEDGEHOG_PORT
    grpc_port = _UNIGRIDCHAIN__gRPC_PORT
    rest_port = _UNIGRIDCHAIN__REST_PORT
    bft_port = _UNIGRIDCHAIN__BFT_PORT
    if not is_port_available(_HEDGEHOG_PORT):
        udp_port = get_random_available_port()
    if not is_port_available(_UNIGRIDCHAIN__gRPC_PORT):
        grpc_port = get_random_available_port()
    if not is_port_available(_UNIGRIDCHAIN__REST_PORT):
        rest_port = get_random_available_port()
    if not is_port_available(_UNIGRIDCHAIN__BFT_PORT):
        bft_port = get_random_available_port()
    print(f"GRPC port Using {grpc_port}")
    print(f"REST port Using {rest_port}")
    print(f"BFT port Using {bft_port}")
    print(f"UDP port Using {udp_port}")
    enable_udp_port(udp_port)
    enable_tcp_port(grpc_port)
    enable_tcp_port(rest_port)
    enable_tcp_port(bft_port)
    version = "0.0.1"

    # Ask for custom locations for hedgehog.bin
    print(
        f"[yellow]The default location of the daemons is {_daemons_path}[yellow]")
    # Ask for custom locations for both daemons
    daemon_choice = input(
        "Would you like to set a custom location for the daemons? (Y/N) ").strip().lower()
    base_path = _daemons_path
    if daemon_choice == 'y':
        daemon_location = input("Enter the custom location for the daemons: ")
        hedgehog_location = os.path.join(daemon_location, "hedgehog.bin")
        base_path = daemon_location
        unigridchain_location = os.path.join(
            daemon_location, f"cosmos-daemond-v{version}-linux-amd64")
    else:
        hedgehog_location = os.path.join(_daemons_path, "hedgehog.bin")
        unigridchain_location = os.path.join(
            _daemons_path, f"cosmos-daemond-v{version}-linux-amd64")
       # Save configuration using named arguments
    hedgehog_log = os.path.join(base_path_chain, "hedgehog.log")
    unigridchain_log = os.path.join(base_path_chain, "unigridchain.log")
    save_config(
        udp_port=_HEDGEHOG_PORT,
        grpc_port=_UNIGRIDCHAIN__gRPC_PORT,
        rest_port=_UNIGRIDCHAIN__REST_PORT,
        bft_port=_UNIGRIDCHAIN__BFT_PORT,
        hedgehog_path=hedgehog_location,
        unigridchain_path=unigridchain_location,
        base_path=base_path,
        log_file_hedgehog=hedgehog_log,
        log_file_cosmos=unigridchain_log
    )
    config = load_configuration()
    print(config)
    try:
        # Check if the hedgehog daemon exists
        if os.path.exists(hedgehog_location):
            # If the daemon exists, run the update command for hedgehog
            update_hedgehog()
        else:
            # If the daemon doesn't exist, download and install hedgehog
            download_and_install(_hedgehog_repo)

        # Check if unigridchain daemon exists using the get_latest_installed_version function
        unigridchain_version = get_latest_installed_version(
            base_path, "cosmos-daemond")
        check_and_create_genesis()
        print(f"Unigridchain version here: {unigridchain_version}")
        if unigridchain_version:
            # If the daemon exists, run the update command for unigridchain
            update_unigridchain()
        else:
            # If the daemon doesn't exist, download and install unigridchain
            download_and_install(_unigridchain_repo)
    except Exception as e:
        print(f"Error: {e}")

    # subprocess.run(["bash", script_path])
    print_important_message("[yellow]Setup complete![/yellow]")
    print_important_message(
        "[yellow]Please run 'source ~/.bashrc' to apply the changes.[/yellow]")


@click.command()
def start():
    """Start the daemons."""
    # Load the configuration from the file specified by $UNIGRID_CONFIG_PATH
    config = load_configuration()
    if config:
        udp_port = config.get('udp_port', 52883)
        grpc_port = config.get('grpc_port', 9090)
        hedgehog_path = config.get(
            'hedgehog_path', '/usr/local/bin/hedgehog.bin')
        unigridchain_path = config.get(
            'unigridchain_path', '/usr/local/bin/cosmos-daemond-v0.0.1-linux-amd64')
        log_file_hedgehog = config.get('log_file_hedgehog')
        log_file_cosmos = config.get('log_file_cosmos')

    # Check if hedgehog daemon exists
    args = [f"--netport={str(udp_port)}"]
    print(f"[green]args: {args}[/green]")
    if os.path.exists(hedgehog_path):
        if not is_hedgehog_running():
            # Start the hedgehog daemon in the background with nohup
            cmd = ["nohup", hedgehog_path, "daemon", args[0]]
            print(f"[green]cmd: {cmd}[/green]")
            # Open the log file in append mode
            with open(log_file_hedgehog, 'a') as log_file:
                subprocess.Popen(cmd, stderr=log_file, stdout=log_file)
            print("[green]Started the hedgehog daemon[/green]")
        else:
            print("[magenta]Hedgehog daemon is already running[/magenta]")

        # Check the local version
        version_cmd = [hedgehog_path, "cli", "--version"]
        local_version = subprocess.run(
            version_cmd, capture_output=True, text=True).stdout.strip().split()[-1]

        # Check the version on GitHub
        github_version = get_github_version(_hedgehog_repo).replace("v", "")

        # Compare versions
        if local_version != github_version:
            print(
                f"[red]Warning: A newer version {github_version} is available on GitHub. You are running {local_version}. Run 'unigridchain-cli update' to update the daemons.[/red]")
    else:
        print(
            f"[red]Hedgehog daemon not found at {hedgehog_path}. Please run 'unigridchain-cli setup' to install it.[/red]")

    # Check if cosmos chain daemon exists
    if unigridchain_path:
        if not is_unigridchain_running(unigridchain_path):
            # Check that the genesis file exists
            check_and_create_genesis()
            # Start the cosmos chain daemon in the background with nohup
            cmd = ["nohup", unigridchain_path, "start"]
            # Open the log file in append mode
            with open(log_file_cosmos, 'a') as log_file:
                subprocess.Popen(cmd, stderr=log_file, stdout=log_file)
            print("[green]Started the cosmos chain daemon[/green]")
        else:
            print("[magenta]Unigrid chain daemon is already running[/magenta]")
    else:
        print(
            f"[red]Cosmos chain daemon not found at {unigridchain_path}. Please run 'unigridchain-cli setup' to install it.[/red]")


@cli.command()
def stop():
    """Stop the daemons."""
    # Check if hedgehog daemon exists
    config = load_configuration()
    if not config:
        print("Error: Could not load configuration.")
        return
    if config:
        hedgehog_path = config.get(
            'hedgehog_path', '/usr/local/bin/hedgehog.bin')
        unigridchain_path = config.get(
            'unigridchain_path', '/usr/local/bin/cosmos-daemond-v0.0.1-linux-amd64')
    if os.path.exists(hedgehog_path):
        if is_hedgehog_running():
            # Stop the hedgehog daemon
            stop_hedgehog_daemon()
        else:
            print("[red]Hedgehog daemon is not running[/red]")
    else:
        print(
            f"[red]Hedgehog daemon not found at {hedgehog_path}. Please run 'unigridchain-cli setup' to install it.[/red]")
    # Check if unigridchain daemon exists using the get_latest_installed_version function
    # unigridchain_version = get_latest_installed_version(
    #     unigridchain_path, _base_unigridchain_name)
    match = re.search(r'-v(\d+\.\d+\.\d+)-', unigridchain_path)
    if match:
        version = match.group(1)
        print(version)
    else:
        print("Version not found in the path.")
    # print(f"Unigridchain version: {unigridchain_version}")
    if version:
        # Assuming you have a function to check if unigridchain is running
        if is_unigridchain_running(unigridchain_path):
            # Assuming you have a function to stop the unigridchain daemon
            # print("[green]Stopping the unigridchain daemon[/green]")
            stop_unigridchain_daemon()
        else:
            print("[red]Unigridchain daemon is not running[/red]")
    else:
        print(
            f"[red]Unigridchain daemon not found in /usr/local/bin. Please run 'unigridchain-cli setup' to install it.[/red]")


@cli.command()
def status():
    """Get the status of both daemons."""
    # Check if hedgehog daemon exists
    config = load_configuration()
    if not config:
        print("Error: Could not load configuration.")
        return
    if config:
        hedgehog_path = config.get(
            'hedgehog_path', '/usr/local/bin/hedgehog.bin')
        unigridchain_path = config.get(
            'unigridchain_path', '/usr/local/bin/cosmos-daemond-v0.0.1-linux-amd64')
    running = is_hedgehog_running()
    if running:
        print("[green]Hedgehog daemon is running[/green]")
    else:
        print("[red]Hedgehog daemon is not running[/red]")
    if is_unigridchain_running(unigridchain_path):
        print("[green]Unigridchain daemon is running[/green]")
    else:
        print("[red]Unigridchain daemon is not running[/red]")

    # Add other daemons as needed


@cli.command()
def update():
    """Directly update the daemons."""
    update_hedgehog()
    update_unigridchain()

# Example usage:
# unigridchain-cli get-balance <address>


@cli.command()
@click.argument('address')
def get_balance(address):
    # use unigridchain-cli get-balance unigrid1565snpkkgxef80pke0n5wp9hu76yuzzapv6894
    """Query the balance of an account on the Unigrid chain."""
    # Replace with your Cosmos SDK chain's REST server endpoint
    url = f"http://localhost:1317/cosmos/bank/v1beta1/balances/{address}"
    response = requests.get(url)
    data = response.json()
    balance = data.get('balances', [{}])[0].get('amount', '0')
    print(f"[yellow]Balance for {address}: {balance} tokens[/yellow]")


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def hedgehog(args):
    """Call the hedgehog daemon."""
    config = load_configuration()
    if not config:
        print("Error: Could not load configuration.")
        return
    if config:
        hedgehog_path = config.get(
            'hedgehog_path', '/usr/local/bin/hedgehog.bin')
    cmd = [hedgehog_path, "cli"]

    if not args:
        cmd.append("--help")
    else:
        cmd.extend(args)
    print(f"Executing command: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout if result.stdout else result.stderr
    print(output)


@cli.command()
def validate():
    """Validates the current setup of the Hedgehog daemon."""

    # Check if daemon is installed
    if not is_daemon_installed():
        print("[red]Hedgehog daemon is not installed. Please run 'unigridchain-cli setup' to install it.[/red]")
        return

    print("[green]Hedgehog daemon is installed.[/green]")

    # Check if version is up-to-date
    local_version = get_version()
    github_version = get_github_version(_hedgehog_repo)
    if local_version != github_version:
        print(
            f"[yellow]Your installed Hedgehog version is {local_version}. A newer version {github_version} is available. Please run 'unigridchain-cli update' to update it.[/yellow]")
        return

    print("[green]Hedgehog daemon is up-to-date.[/green]")


cli.add_command(hedgehog)
cli.add_command(setup)
cli.add_command(start)

if __name__ == "__main__":
    cli()
