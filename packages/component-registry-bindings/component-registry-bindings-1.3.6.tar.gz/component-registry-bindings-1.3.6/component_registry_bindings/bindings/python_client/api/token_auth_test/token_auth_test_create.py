from typing import Any, Dict, Optional, Union

import requests

from ...client import AuthenticatedClient
from ...models.token_auth_test_create_response_200 import TokenAuthTestCreateResponse200
from ...types import UNSET, Response, Unset

QUERY_PARAMS = {}


def _get_kwargs(
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/token_auth_test".format(
        client.base_url,
    )

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
    }


def _parse_response(
    *, response: requests.Response
) -> Optional[Union[Any, TokenAuthTestCreateResponse200]]:
    if response.status_code == 200:
        _response_200 = response.json()
        response_200: TokenAuthTestCreateResponse200
        if isinstance(_response_200, Unset):
            response_200 = UNSET
        else:
            response_200 = TokenAuthTestCreateResponse200.from_dict(_response_200)

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(
    *, response: requests.Response
) -> Response[Union[Any, TokenAuthTestCreateResponse200]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, TokenAuthTestCreateResponse200]]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = requests.post(
        verify=client.verify_ssl,
        auth=client.auth,
        timeout=client.timeout,
        **kwargs,
    )
    response.raise_for_status()

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, TokenAuthTestCreateResponse200]]:
    """View to test authentication with DRF Tokens."""

    return sync_detailed(
        client=client,
    ).parsed


async def async_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, TokenAuthTestCreateResponse200]]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with client.get_async_session().post(
        verify_ssl=client.verify_ssl, raise_for_status=True, **kwargs
    ) as response:
        content = await response.read()
        resp = requests.Response()
        resp.status_code = response.status
        resp._content = content

    return _build_response(response=resp)


async def async_(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, TokenAuthTestCreateResponse200]]:
    """View to test authentication with DRF Tokens."""

    return (
        await async_detailed(
            client=client,
        )
    ).parsed
