import click

from qwak_sdk.commands.workspaces.delete._logic import _delete_workspace
from qwak_sdk.inner.tools.cli_tools import QwakCommand


@click.command("delete", cls=QwakCommand)
@click.option(
    "--workspace-id",
    required=True,
    metavar="WORKSPACE-ID",
    help="The id of the workspace",
)
def delete_workspace(workspace_id: str, **kwargs):
    _delete_workspace(workspace_id=workspace_id)
