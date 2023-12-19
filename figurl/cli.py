import click

# ------------------------------------------------------------
# Preserve figure
# ------------------------------------------------------------
@click.command(help='Preserve a figurl figure')
@click.argument('figurl_url')
@click.option('--output-folder', required=True, help='Output folder')
def preserve(figurl_url: str, output_folder: str):
    from .preserve.preserve import preserve
    preserve(figurl_url=figurl_url, output_folder=output_folder)

# ------------------------------------------------------------
# Main cli
# ------------------------------------------------------------
@click.group(help="dendro command line interface")
def main():
    pass

main.add_command(preserve)
