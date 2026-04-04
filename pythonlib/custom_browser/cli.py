#!/usr/bin/env python3
"""Command-line interface for the Custom Antidetect Browser."""

import json
from typing import Optional

import click

from .fingerprint_generator import FingerprintGenerator
from .launcher import BrowserLauncher
from .profile_manager import ProfileManager


@click.group()
def main():
    """Custom Antidetect Browser - Professional fingerprint management."""
    pass


@main.command()
@click.option("--name", required=True, help="Profile name")
@click.option("--os", "os_type", default="windows", help="Target OS (windows/macos/linux)")
@click.option("--proxy", help="Proxy URL (optional)")
def create(name: str, os_type: str, proxy: Optional[str]):
    """Create a new browser profile."""
    click.echo(f"Creating profile: {name}")

    # Generate fingerprint
    fingerprint = FingerprintGenerator.generate_for_os(os_type)

    # Parse proxy if provided
    proxy_config = None
    if proxy:
        # Simple proxy parsing (expand as needed)
        proxy_config = {"url": proxy}

    # Create profile
    profile_id = ProfileManager.create_profile(name, fingerprint, proxy_config)
    click.echo(f"✅ Profile created successfully!")
    click.echo(f"   ID: {profile_id}")
    click.echo(f"   Name: {name}")
    click.echo(f"   OS: {os_type}")


@main.command()
@click.argument("profile_id")
def launch(profile_id: str):
    """Launch a browser with the specified profile."""
    click.echo(f"Launching profile: {profile_id}")

    # Load profile to verify it exists
    try:
        profile = ProfileManager.load_profile(profile_id)
        click.echo(f"   Profile: {profile['name']}")
        BrowserLauncher.launch(profile_id)
        click.echo("✅ Browser launched successfully!")
    except FileNotFoundError:
        click.echo(f"❌ Profile not found: {profile_id}")


@main.command()
def list():
    """List all available profiles."""
    profiles = ProfileManager.list_profiles()

    if not profiles:
        click.echo("No profiles found.")
        return

    click.echo(f"\n📋 Available Profiles ({len(profiles)}):")
    click.echo("-" * 50)
    for profile in profiles:
        click.echo(f"  ID: {profile['id']}")
        click.echo(f"  Name: {profile['name']}")
        click.echo(f"  OS: {profile['fingerprint'].get('platform', 'unknown')}")
        click.echo("-" * 50)


@main.command()
@click.argument("profile_id")
def delete(profile_id: str):
    """Delete a profile."""
    click.echo(f"Deleting profile: {profile_id}")
    if ProfileManager.delete_profile(profile_id):
        click.echo("✅ Profile deleted successfully!")
    else:
        click.echo("❌ Profile not found.")


@main.command()
@click.argument("profile_id")
def info(profile_id: str):
    """Show detailed information about a profile."""
    try:
        profile = ProfileManager.load_profile(profile_id)
        click.echo(f"\n📊 Profile Information:")
        click.echo(f"  ID: {profile['id']}")
        click.echo(f"  Name: {profile['name']}")
        click.echo(f"\n  Fingerprint:")
        for key, value in profile["fingerprint"].items():
            click.echo(f"    {key}: {value}")
        if profile.get("proxy"):
            click.echo(f"\n  Proxy: {profile['proxy'].get('url', 'N/A')}")
    except FileNotFoundError:
        click.echo(f"❌ Profile not found: {profile_id}")


if __name__ == "__main__":
    main()
