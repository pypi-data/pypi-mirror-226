import os
import json

CONFIG_DIR = os.path.expanduser("~/.config/dakka")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def ensure_config_dir():
    """Ensure that the configuration directory exists."""
    os.makedirs(CONFIG_DIR, exist_ok=True)


def read_config():
    """Read the configuration from the config file."""
    ensure_config_dir()
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None


def save_spec_to_config(spec, name, config):
    """Save an OpenAPI spec to the global configuration."""
    config["specs"][name] = spec

def get_spec_from_config(name, config):
    """Get an OpenAPI spec from the global configuration."""
    return config["specs"].get(name, None)

def delete_spec_from_config(name, config):
    """Delete an OpenAPI spec from the global configuration."""
    del config["specs"][name]

def get_enabled_specs_from_profile(profile_name, config):
    """Get the enabled specs for a profile."""
    return get_user_profile(profile_name, config).get("enabled_specs", [])

def get_user_profile(profile_name, config):
    """Get the user profile"""
    return config["profiles"].get(profile_name, {})

def enable_spec_in_profile(spec_name, config_name, config):
    """Enable an OpenAPI spec in a profile."""
    profile = get_user_profile(config_name, config)
    if spec_name not in profile["enabled_specs"]:
        profile["enabled_specs"].append(spec_name)

def disable_spec_in_profile(spec_name, profile_name, config):
    """Disable an OpenAPI spec in a profile."""
    profile = get_user_profile(profile_name, config)
    if spec_name in profile["enabled_specs"]:
        config["enabled_specs"].remove(spec_name)

def write_config(config):
    """Write the configuration to the config file."""
    ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def get_specs(specs, config):
    """Get the specs"""
    full_specs = []
    for spec in specs:
        full_spec = get_spec_from_config(spec, config)
        if full_spec is not None:
            full_specs.append(full_spec)
        else:
            raise ValueError(f"Spec '{spec}' not found. Please disable in user profile or install globally.")
    return full_specs