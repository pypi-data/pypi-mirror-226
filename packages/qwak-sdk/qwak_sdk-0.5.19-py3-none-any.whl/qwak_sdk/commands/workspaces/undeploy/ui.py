import click

from qwak_sdk.commands.workspaces.undeploy._logic import _undeploy_workspace
from qwak_sdk.inner.tools.cli_tools import QwakCommand


@click.command("undeploy", cls=QwakCommand)
@click.option(
    "--workspace-id",
    required=True,
    metavar="WORKSPACE-ID",
    help="The id of the workspace",
)
def undeploy_workspace(workspace_id: str, **kwargs):
    _undeploy_workspace(workspace_id=workspace_id)
