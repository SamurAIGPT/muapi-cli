from .client import (
    get_result,
    wait_for_result,
)


class PredictionsAPI:
    def get(self, request_id: str):
        return get_result(request_id)

    def wait(self, request_id: str):
        return wait_for_result(request_id)