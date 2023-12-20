import click

# ------------------------------------------------------------
# Preserve figure
# ------------------------------------------------------------
@click.command(help='Preserve a figurl figure')
@click.argument('figurl_url')
@click.argument('output-file')
def preserve_figure(figurl_url: str, output_file: str):
    from .preserve.preserve_figure import preserve_figure as _preserve_figure
    _preserve_figure(figurl_url=figurl_url, output_file=output_file)

# ------------------------------------------------------------
# Serve a preserved figure
# ------------------------------------------------------------
@click.command(help='Serve a preserved figurl figure')
@click.argument('input-file')
@click.option('--port', type=int, default=8000, help='Port')
def serve_figure(input_file: str, port: int):
    from .preserve.serve_figure import serve_figure as _serve_figure
    _serve_figure(input_file=input_file, port=port)

# Maybe at some point we'll want to do this. But for now there is no use case for it.
# # ------------------------------------------------------------
# # Zenodo upload folder
# # ------------------------------------------------------------
# @click.command(help='Upload a folder to Zenodo')
# @click.argument('source-folder')
# @click.option('--record-id', required=True, help='Zenodo record ID (must be a draft)')
# @click.option('--sandbox', is_flag=True, help='Use Zenodo sandbox')
# @click.option('--dest', required=True, help='Destination folder within the record')
# def zenodo_upload_folder(source_folder: str, record_id: str, sandbox: bool, dest: str):
#     from .preserve.zenodo_upload_folder import zenodo_upload_folder as _zenodo_upload_folder
#     _zenodo_upload_folder(source_folder=source_folder, record_id=record_id, sandbox=sandbox, dest=dest)

# ------------------------------------------------------------
# Main cli
# ------------------------------------------------------------
@click.group(help="dendro command line interface")
def main():
    pass

main.add_command(preserve_figure)
main.add_command(serve_figure)
