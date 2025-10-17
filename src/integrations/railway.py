import httpx
from src.core.config import settings

class RailwayClient:
    def __init__(self):
        self.base_url = settings.RAILWAY_API_URL
        self.headers = {
            "Authorization": f"Bearer {settings.RAILWAY_API_KEY}",
            "Content-Type": "application/json"
        }
        self.client = httpx.AsyncClient(headers=self.headers)
    
    async def get_build_logs(self, build_id: str) -> str:
        """Get build logs from Railway"""
        try:
            response = await self.client.get(
                f"{self.base_url}/builds/{build_id}/logs"
            )
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error getting Railway build logs: {str(e)}")
            return ""
    
    async def get_deployment_status(self, deployment_id: str) -> dict:
        """Get deployment status from Railway"""
        try:
            response = await self.client.get(
                f"{self.base_url}/deployments/{deployment_id}"
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting Railway deployment status: {str(e)}")
            return {}