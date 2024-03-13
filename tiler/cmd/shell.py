import click

from tiler.cmd import pass_state_context

@click.group(
    help="Debian installer."
)
@pass_state_context
def cli(state):
    pass

def main():
    cli(prog_name="tiler")

