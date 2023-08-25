from qwak.clients.workspace_manager import WorkspaceManagerClient


def _undeploy_workspace(workspace_id: str, **kwargs):
    """
    Undeploy an existing workspace
    Args:
    workspace_id: The id of the workspace to deploy
    """
    print(f"Undeploy an existing workspace with id {workspace_id}")
    workspace_manager_client = WorkspaceManagerClient()
    workspace_manager_client.undeploy_workspace(workspace_id=workspace_id)

    print(f"Workspace {workspace_id} was undeployed successfully")
