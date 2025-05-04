import rich_click as click
import subprocess
import os
from functools import wraps
from typing import List, Callable
from click import style
from pathlib import Path
from inspect import signature
from dotenv import load_dotenv
from azure.identity import AzureDeveloperCliCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

load_dotenv()

# Add these constants near the top
TEMP_FILE = Path.home() / '.lab_setup_progress'
# Step registration
steps: List[tuple[Callable, str]] = []

def blue(text: str):
    return style(text, fg="blue")

def bold(text: str):
    return style(text, fg="bright_white", bold=True)

def step(label: str):
    """Decorator to register and label setup steps"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, step_number, total_steps, **kwargs):
            click.echo(f"\n{bold(f'Step {step_number}/{total_steps}')}: {blue(label)}")
            click.echo()
            return func(*args, **kwargs)
        steps.append((wrapper, label))
        return wrapper
    return decorator

@step("Azure Developer CLI Authentication")
def azd_login(*, username: str = None, password: str = None, tenant: str = None, force: bool = False):
    """Authenticate with Azure Developer CLI using device code"""
    # Display credentials if provided
    if username and password:
        opts = {'underline': True}
        click.echo(f"{style('When asked to ', **opts)}{style('Pick an account', **opts, bold=True)}{style(', hit the ', **opts)}{style('Use another account', **opts, bold=True)}{style(' button and enter the following:', **opts)}")
        click.echo(f"Username: {style(username, fg='blue', bold=True)}")
        click.echo(f"Password: {style(password, fg='blue', bold=True)}")
        click.echo()
        click.echo(f"{style('IMPORTANT', fg='red', reverse=True)}: {style('DO NOT use your personal credentials for this step!', fg='red', underline=True)}")
        click.echo()
    
    # Proceed with authentication
    login_cmd = ['azd', 'auth', 'login', '--use-device-code', '--no-prompt']
    if tenant:
        login_cmd.extend(['--tenant-id', tenant])
    subprocess.run(login_cmd, check=True)

@step("Azure Developer CLI Environment Setup")
def create_azd_environment(*, azure_env_name: str, subscription: str):
    # Check if environment already exists
    result = subprocess.run(
        ['azd', 'env', 'list'],
        capture_output=True,
        text=True,
        check=True
    )
    
    if azure_env_name in result.stdout:
        click.echo(f"Environment '{azure_env_name}' already exists")
        return
        
    # Create new environment if it doesn't exist
    azd_cmd = [
        'azd', 'env', 'new', azure_env_name,
        '--location', 'eastus2',
        '--subscription', subscription
    ]
    subprocess.run(azd_cmd, check=True)

@step("Refresh AZD Environment")
def refresh_environment(*, azure_env_name: str):
    subprocess.run([
        'azd', 'env', 'refresh',
        '-e', azure_env_name,
        '--no-prompt'
    ], check=True)

@step("Export Environment Variables")
def export_variables():
    # Get the directory where the script is located and resolve .env path
    env_path = Path(__file__).parent / '.env'
    
    with open(env_path, 'w') as env_file:
        subprocess.run(['azd', 'env', 'get-values'], stdout=env_file, check=True)

@step("Add DeepSeek Key")
def add_variables():
    # Get the directory where the script is located and resolve .env path
    env_path = Path(__file__).parent / '.env'

    load_dotenv(env_path)
    
    sub_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    name = os.getenv("AI_SERVICES_NAME")
    resource_group = f"{os.getenv("AZURE_ENV_NAME")}-rg"

    # 1. authenticate with whatever azd/az login cached
    cred = AzureDeveloperCliCredential()       # works for users + azd pipelines

    # 2. call the management plane
    mgmt = CognitiveServicesManagementClient(cred, sub_id)
    keys = mgmt.accounts.list_keys(resource_group, name)  # ⇐ ARM call
    key = keys.key1 
    
    # Read existing content to check if variable is already there
    content = env_path.read_text() if env_path.exists() else ""
    
    # Check if TAVILY_API_KEY is already in the file
    if "AZURE_AI_API_KEY=" not in content:
        # Open in append mode and add the variable
        with open(env_path, 'a') as env_file:
            # Add a newline if the file isn't empty and doesn't end with newline
            if content and not content.endswith('\n'):
                env_file.write('\n')
            env_file.write(f'AZURE_AI_API_KEY="{key}"\n')
        print(f"added key to env file")
    else:
        print("AZURE_AI_API_KEY already exists in .env file")

@step("Complete env file")
def add_env_var():
    # Get path to .env file at the project root
    env_path = Path(__file__).parent / '.env'
    
    # Check if file exists break 
    if not env_path.exists():
        print(f"env file does not exist")
        return
         
    # Read existing content to check if variable is already there
    content = env_path.read_text() if env_path.exists() else ""
    
    # Check if TAVILY_API_KEY is already in the file
    if "TAVILY_API_KEY=" not in content:
        # Open in append mode and add the variable
        with open(env_path, 'a') as env_file:
            # Add a newline if the file isn't empty and doesn't end with newline
            if content and not content.endswith('\n'):
                env_file.write('\n')
            env_file.write('TAVILY_API_KEY=""\n')
        print(f"You can find your .env file in the src folder!")
    else:
        print("TAVILY_API_KEY already exists in .env file")

@click.command()
@click.option('--username', help='Azure username/email for authentication')
@click.option('--password', help='Azure password for authentication', hide_input=True)
@click.option('--azure-env-name', required=True, help='Name for the new Azure environment')
@click.option('--subscription', required=True, help='Azure subscription ID to use')
@click.option('--tenant', help='Azure tenant ID')
@click.option('--force', is_flag=True, help='Force re-authentication and start from beginning')
@click.option('--step', type=int, help='Resume from a specific step number (1-based)')
def setup(username, password, azure_env_name, subscription, tenant, force, step):
    """
    Automates Azure environment setup and configuration.
    
    This command will:
    - Azure Developer CLI Authentication
    - Azure Developer CLI Environment Setup
    - Refresh AZD Environment
    - Export Environment Variables
    """
    try:
        # Create parameters dictionary
        params = {
            'username': username,
            'password': password,
            'azure_env_name': azure_env_name,
            'subscription': subscription,
            'tenant': tenant,
            'force': force
        }
        
        # Determine starting step
        start_step = 0
        if step is not None:
            if not 1 <= step <= len(steps):
                raise click.BadParameter(f"Step must be between 1 and {len(steps)}")
            start_step = step - 1
        elif not force and TEMP_FILE.exists():
            start_step = int(TEMP_FILE.read_text().strip())
            if start_step >= len(steps):
                click.echo("\nAll steps were already successfully executed!")
                click.echo("Use --force to execute all steps from the beginning if needed.")
                return
            click.echo(f"\nResuming from step {blue(start_step + 1)}")
        
        # Execute all registered steps
        for index, entry in enumerate(steps):
            # Skip steps that were already completed
            if index < start_step:
                continue
                
            step_func, _ = entry
            # Get the parameter names for this function
            sig = signature(step_func.__wrapped__)
            # Filter params to only include what the function needs
            step_params = {
                name: params[name] 
                for name in sig.parameters
                if name in params
            }
            # Execute step and merge any returned dict into params
            result = step_func(step_number=index + 1, total_steps=len(steps), **step_params)
            if isinstance(result, dict):
                params.update(result)
            
            # Save progress after each successful step
            TEMP_FILE.write_text(str(index + 1))
        
        # Clean up temp file on successful completion
        if TEMP_FILE.exists():
            TEMP_FILE.unlink()
        
        click.echo("\nSetup completed successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error during setup: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    setup()

# ++./docs/workshop/lab_setup.py --username '@lab.CloudPortalCredential(User1).Username' # --password '@lab.CloudPortalCredential(User1).Password' # --azure-env-name 'AITOUR@lab.LabInstance.Id' --subscription '@lab.CloudSubscription.Id'++
