from typing import Optional, Dict, Tuple, Union
from imagine.remote.http_client import HttpClient
from imagine.utils.imports.dynamic import dynamic_import


class TestRequestClient(HttpClient):
    __base_url: str = "https://api.vyro.ai/v1/imagine/api"

    def post(
        self,
        endpoint: str,
        parameters: Dict[str, Union[int, float, str]],
        files: Optional[Dict[str, bytes]] = None,
        headers: Dict[str, str] = None,
    ) -> Tuple[int, bytes]:
        requests = dynamic_import("requests")
        if requests is None:
            return (1000, b"Module requests could not be loaded.")

        url = self.__base_url + endpoint

        response = requests.post(
            url, headers=headers, data=parameters, files=files, timeout=180
        )

        return (response.status_code, response.content)
