from typing import List
import httpx
from src.core.config import settings

class GitHubClient:
    def __init__(self):
        self.base_url = settings.GITHUB_API_URL
        self.headers = {
            "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.client = httpx.AsyncClient(headers=self.headers)
    
    async def commit_and_push(self, files: List[str], message: str) -> bool:
        """Commit and push changes to GitHub"""
        try:
            # Get current commit SHA
            response = await self.client.get(
                f"{self.base_url}/repos/{settings.REPO_OWNER}/{settings.REPO_NAME}/git/ref/heads/{settings.MAIN_BRANCH}"
            )
            response.raise_for_status()
            current_sha = response.json()["object"]["sha"]
            
            # Create tree with modified files
            tree_items = []
            for file_path in files:
                with open(file_path, "r") as f:
                    content = f.read()
                
                # Create blob
                blob_data = {
                    "content": content,
                    "encoding": "utf-8"
                }
                blob_response = await self.client.post(
                    f"{self.base_url}/repos/{settings.REPO_OWNER}/{settings.REPO_NAME}/git/blobs",
                    json=blob_data
                )
                blob_response.raise_for_status()
                
                tree_items.append({
                    "path": file_path,
                    "mode": "100644",
                    "type": "blob",
                    "sha": blob_response.json()["sha"]
                })
            
            # Create tree
            tree_data = {
                "base_tree": current_sha,
                "tree": tree_items
            }
            tree_response = await self.client.post(
                f"{self.base_url}/repos/{settings.REPO_OWNER}/{settings.REPO_NAME}/git/trees",
                json=tree_data
            )
            tree_response.raise_for_status()
            
            # Create commit
            commit_data = {
                "message": message,
                "tree": tree_response.json()["sha"],
                "parents": [current_sha]
            }
            commit_response = await self.client.post(
                f"{self.base_url}/repos/{settings.REPO_OWNER}/{settings.REPO_NAME}/git/commits",
                json=commit_data
            )
            commit_response.raise_for_status()
            
            # Update reference
            ref_data = {
                "sha": commit_response.json()["sha"],
                "force": True
            }
            ref_response = await self.client.patch(
                f"{self.base_url}/repos/{settings.REPO_OWNER}/{settings.REPO_NAME}/git/refs/heads/{settings.MAIN_BRANCH}",
                json=ref_data
            )
            ref_response.raise_for_status()
            
            return True
        except Exception as e:
            print(f"Error pushing to GitHub: {str(e)}")
            return False
    
    async def get_file_content(self, file_path: str, ref: str = None) -> str:
        """Get file content from GitHub"""
        try:
            params = {"ref": ref} if ref else {}
            response = await self.client.get(
                f"{self.base_url}/repos/{settings.REPO_OWNER}/{settings.REPO_NAME}/contents/{file_path}",
                params=params
            )
            response.raise_for_status()
            return response.json()["content"]
        except Exception as e:
            print(f"Error getting file from GitHub: {str(e)}")
            return ""