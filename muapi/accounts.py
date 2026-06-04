import httpx

from .config import BASE_URL, get_api_key
from .client import MuapiError


class AccountAPI:
    def _headers(self):
        key = get_api_key()

        if not key:
            raise MuapiError(
                "No API key configured. Run: muapi auth configure"
            )

        return {"x-api-key": key}

    def balance(self):
        resp = httpx.get(
            f"{BASE_URL}/account/balance",
            headers=self._headers(),
            timeout=30.0,
        )

        if resp.status_code >= 400:
            raise MuapiError(resp.text, resp.status_code)

        return resp.json()

    def topup(
        self,
        amount: int,
        currency: str = "usd",
    ):
        resp = httpx.post(
            f"{BASE_URL}/account/topup",
            json={
                "amount": amount,
                "currency": currency.lower(),
            },
            headers=self._headers(),
            timeout=30.0,
        )

        if resp.status_code >= 400:
            raise MuapiError(resp.text, resp.status_code)

        return resp.json()