import click

from qwak_sdk.commands.workspaces.deploy._logic import _deploy_workspace
from qwak_sdk.inner.tools.cli_tools import QwakCommand


@click.command("deploy", cls=QwakCommand)
@click.option(
    "--workspace-id",
    required=True,
    metavar="WORKSPACE-ID",
    help="The id of the workspace",
)
def deploy_workspace(workspace_id: str, **kwargs):
    _deploy_workspace(workspace_id=workspace_id)
