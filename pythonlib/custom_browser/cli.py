#!/usr/bin/env python3
"""CLI for Custom Antidetect Browser - manage multiple profiles."""

import json
from typing import Optional

import click

from .fingerprint_generator import FingerprintGenerator  # optional, for custom fingerprints
from .launcher import BrowserLauncher
from .profile_manager import ProfileManager


@click.group()
def cli():
    """Custom Antidetect Browser – Professional profile management."""
    pass


@cli.command()
@click.option("--name", "-n", required=True, help="Profile name")
@click.option("--proxy", "-p", help="Proxy URL (e.g., http://user:pass@host:port)")
@click.option("--os", "os_type", default="windows", help="Target OS hint (windows/macos/linux)")
@click.option("--custom-fingerprint", help="Path to JSON file with custom fingerprint overrides")
def create(name: str, proxy: Optional[str], os_type: str, custom_fingerprint: Optional[str]):
    """Create a new browser profile."""
    proxy_dict = None
    if proxy:
        proxy_dict = {"url": proxy}

    fingerprint_override = None
    if custom_fingerprint:
        with open(custom_fingerprint, "r") as f:
            fingerprint_override = json.load(f)

    profile_id = ProfileManager.create_profile(
        name=name, proxy=proxy_dict, custom_fingerprint=fingerprint_override
    )
    click.echo(f"✅ Profile created: {name} (ID: {profile_id})")


@cli.command()
def list():
    """List all existing profiles."""
    profiles = ProfileManager.list_profiles()
    if not profiles:
        click.echo("No profiles found. Create one with `custom-browser create`")
        return
    click.echo("\n📋 Available profiles:")
    click.echo("-" * 60)
    for p in profiles:
        click.echo(f"  ID: {p['id']}")
        click.echo(f"  Name: {p['name']}")
        click.echo(f"  Created: {p['created_at']}")
        click.echo(f"  Proxy: {'yes' if p['has_proxy'] else 'no'}")
        click.echo("-" * 60)


@cli.command()
@click.argument("identifier")  # can be id or name
@click.option("--headless", is_flag=True, help="Run in headless mode")
@click.option("--block-images", is_flag=True, help="Block images to save bandwidth")
@click.option("--block-webrtc", default=True, help="Block WebRTC leaks")
def launch(identifier: str, headless: bool, block_images: bool, block_webrtc: bool):
    """Launch a browser with the specified profile (by ID or name)."""
    # Try to find profile by ID first, then by name
    profile = None
    try:
        profile = ProfileManager.load_profile(identifier)
    except FileNotFoundError:
        # search by name
        all_profiles = ProfileManager.list_profiles()
        matching = [p for p in all_profiles if p["name"] == identifier]
        if matching:
            profile = ProfileManager.load_profile(matching[0]["id"])
        else:
            click.echo(f"❌ Profile not found: {identifier}")
            return

    click.echo(f"🚀 Launching profile: {profile['name']}")
    BrowserLauncher.launch(
        profile_data=profile,
        headless=headless,
        block_images=block_images,
        block_webrtc=block_webrtc,
    )


@cli.command()
@click.argument("identifier")
def delete(identifier: str):
    """Delete a profile (by ID or name)."""
    # Find profile ID
    profile_id = identifier
    try:
        ProfileManager.load_profile(identifier)
    except FileNotFoundError:
        all_profiles = ProfileManager.list_profiles()
        matching = [p for p in all_profiles if p["name"] == identifier]
        if matching:
            profile_id = matching[0]["id"]
        else:
            click.echo(f"❌ Profile not found: {identifier}")
            return

    if click.confirm(f"Are you sure you want to delete profile '{identifier}'?"):
        if ProfileManager.delete_profile(profile_id):
            click.echo(f"✅ Profile deleted: {identifier}")
        else:
            click.echo(f"❌ Failed to delete profile")


@cli.command()
@click.argument("identifier")
def info(identifier: str):
    """Show detailed profile information."""
    try:
        profile = ProfileManager.load_profile(identifier)
    except FileNotFoundError:
        all_profiles = ProfileManager.list_profiles()
        matching = [p for p in all_profiles if p["name"] == identifier]
        if matching:
            profile = ProfileManager.load_profile(matching[0]["id"])
        else:
            click.echo(f"❌ Profile not found: {identifier}")
            return

    click.echo(f"\n🔍 Profile: {profile['name']}")
    click.echo(f"  ID: {profile['id']}")
    click.echo(f"  Created: {profile.get('created_at')}")
    click.echo(f"  Proxy: {profile.get('proxy', {}).get('url', 'None')}")
    click.echo(f"  Custom fingerprint: {'yes' if profile.get('custom_fingerprint') else 'no'}")
    if profile.get("custom_fingerprint"):
        click.echo("  Overrides:")
        for k, v in profile["custom_fingerprint"].items():
            click.echo(f"    {k}: {v}")


if __name__ == "__main__":
    cli()
