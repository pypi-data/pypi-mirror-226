import click
import requests
import os
import json
import yaml

from dakka.utils import delete_spec_from_config, disable_spec_in_profile, enable_spec_in_profile, get_enabled_specs_from_profile, get_specs, read_config, write_config, save_spec_to_config, get_spec_from_config
from dakka.ask import process_question


from openapi_spec_validator import validate_spec

@click.group()
def main():
    """Dakka - Talk to an AI agent that uses OpenAI specs to answer questions."""
    pass


@main.command()
def install():
    """Install Dakka and set up configurations."""
    openai_key = input("Enter your OpenAI key: ")
    config = {
        "openai_key": openai_key,
        "default_profile": "default",
        "profiles": {
            "default": {
                "enabled_specs": [],
            }
        },
        "specs": {}
    }
    write_config(config)
    print("Configuration saved.")

@main.group()
def config():
    """Manage configuration settings."""
    pass

@config.command()
@click.argument("name", type=str)
def delete(name):
    """Delete an existing spec by name."""
    config = read_config()

    # Check if the spec exists.
    if get_spec_from_config(name, config) is None:
        print(f"A spec with the name '{name}' does not exist.")
        return

    # Delete the spec.
    delete_spec_from_config(name, config)
    write_config(config)
    print(f"Spec '{name}' deleted.")

@config.command()
@click.argument("url_or_path", type=str)
@click.option("--name", type=str, default=None, help="Name for the spec. Defaults to the file name.")
@click.option("-f", "--force", is_flag=True, help="Override an existing spec with the same name.")
def save(url_or_path, name, force):
    """Save an OpenAPI spec from a URL or a file path."""
    # Check if it's a URL or a file path.
    if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
        response = requests.get(url_or_path)
        response.raise_for_status()
        spec = yaml.load(response.text(), Loader=yaml.FullLoader)
    else:
        with open(url_or_path, "r") as f:
            spec = yaml.load(f, Loader=yaml.FullLoader)

    # Validate the OpenAPI spec
    try:
        validate_spec(spec)
    except Exception as e:
        print(f"Invalid OpenAPI spec: {e}")
        return

    # Set the spec name.
    if not name:
        if "info" in spec and "title" in spec["info"]:
            name = spec["info"]["title"]
        name = os.path.splitext(os.path.basename(url_or_path))[0]

    # Check if a spec with the same name already exists.
    config = read_config()
    if not force and get_spec_from_config(name, config) is not None:
        print(f"A spec with the name '{name}' already exists. Please choose a different name.")
        return

    # Save the spec in the config.
    config = read_config()
    save_spec_to_config(spec, name, config)
    write_config(config)
    print(f"Spec '{name}' saved.")


@config.command()
@click.argument("spec_name", type=str)
@click.option("-p", "--profile", type=str, default="default", help="Specify a different user profile.")
def enable(spec_name, profile):
    """Enable an OpenAPI spec."""
    config = read_config()
    enable_spec_in_profile(spec_name, profile, config)
    write_config(config)
    print(f"Spec '{spec_name}' enabled in '{profile}'.")


@config.command()
@click.argument("spec_name", type=str)
@click.option("-p", "--profile", type=str, default="default", help="Specify a different user profile.")
def disable(spec_name, profile):
    """Disable an OpenAPI spec."""
    config = read_config()
    disable_spec_in_profile(spec_name, profile, config)
    print(f"Spec '{spec_name}' disabled in '{profile}'.")


@config.command()
@click.argument("config_name", type=str)
def switch(config_name):
    """Switch to a different configuration."""
    config = read_config()
    if config_name in config["profiles"]:
        config["default_profile"] = config_name
        write_config(config)
        print(f"Switched to config '{config_name}'.")
    else:
        print(f"Config '{config_name}' not found.")

@config.command()
@click.argument("config_name", type=str)
def default(config_name):
    """Set the default configuration."""
    config = read_config()
    if config_name in config["profiles"]:
        config["default_profile"] = config_name
        write_config(config)
        print(f"Default config set to '{config_name}'.")
    else:
        print(f"Config '{config_name}' not found.")


@main.command()
@click.argument("question", type=str)
@click.option("-c", "--config-name", type=str, help="Specify a different config.")
def ask(question, config_name):
    """Ask a question and get a response from the AI agent."""
    config = read_config()
    
    # Use the specified config or the default config.
    current_profile = config_name or config["default_profile"]
    
    # Process the question and determine the endpoint.
    enabled_specs = get_enabled_specs_from_profile(current_profile, config)
    loaded_specs = get_specs(enabled_specs, config)
    conversation = process_question(question, loaded_specs, config)
    
    print("Response:", conversation[-1]['content'])

@config.command(name="list-profiles")
def list_profiles():
    """List all available user profiles."""
    config = read_config()
    configs = list(config["profiles"].keys())
    print("Available profiles:", ", ".join(configs))

@config.command(name="list-specs")
@click.option("-p", "--profile", type=str, help="Specify a different profile.")
@click.option("-a", "--all", is_flag=True, help="List all installed specs.")
def list_specs(profile, all):
    """List all installed specs for a specified profile or all known specs"""
    config = read_config()
    
    # Use the specified config or the default config.
    if not all:
        current_profile = profile or config["default_profile"]
        
        if current_profile not in config["profiles"]:
            print(f"Profile '{current_profile}' not found.")
            return
        
        specs = get_enabled_specs_from_profile(current_profile, config)
        print(f"Installed specs for config '{current_profile}':", ", ".join(specs))
    else:
        specs = list(config["specs"].keys())
        print("All installed specs are:", ", ".join(specs))
