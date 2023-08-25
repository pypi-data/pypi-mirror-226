from qwak.clients.workspace_manager import WorkspaceManagerClient


def _deploy_workspace(workspace_id: str, **kwargs):
    """
    Deploying an existing workspace
    Args:
    workspace_id: The id of the workspace to deploy
    """
    print(f"Deploying an existing workspace with id {workspace_id}")
    workspace_manager_client = WorkspaceManagerClient()
    workspace_manager_client.deploy_workspace(workspace_id=workspace_id)

    print(f"Workspace {workspace_id} was deployed successfully")
