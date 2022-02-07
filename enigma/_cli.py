import click
from enigma._gui_wrapper import main


@click.command()
def start_gui():
    """start the enigma emulator gui"""
    main()
