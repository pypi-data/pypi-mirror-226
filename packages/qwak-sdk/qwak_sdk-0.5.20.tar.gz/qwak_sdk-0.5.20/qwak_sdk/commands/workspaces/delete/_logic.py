from qwak.clients.workspace_manager import WorkspaceManagerClient


def _delete_workspace(workspace_id: str, **kwargs):
    """
    Deleting workspace
    Args:
    workspace_id: The id of the workspace to delete
    """

    print(f"Deleting an existing workspace with id {workspace_id}")
    workspace_manager_client = WorkspaceManagerClient()
    workspace_manager_client.delete_workspace(workspace_id=workspace_id)

    print(f"Workspace {workspace_id} was deleted successfully")
