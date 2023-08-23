from typing import Any, Dict, Optional

import requests

from ...client import Client
from ...models.controlled_access_test_retrieve_response_200 import (
    ControlledAccessTestRetrieveResponse200,
)
from ...types import UNSET, Response, Unset

QUERY_PARAMS = {}


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/api/controlled_access_test".format(
        client.base_url,
    )

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
    }


def _parse_response(
    *, response: requests.Response
) -> Optional[ControlledAccessTestRetrieveResponse200]:
    if response.status_code == 200:
        _response_200 = response.json()
        response_200: ControlledAccessTestRetrieveResponse200
        if isinstance(_response_200, Unset):
            response_200 = UNSET
        else:
            response_200 = ControlledAccessTestRetrieveResponse200.from_dict(
                _response_200
            )

        return response_200
    return None


def _build_response(
    *, response: requests.Response
) -> Response[ControlledAccessTestRetrieveResponse200]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[ControlledAccessTestRetrieveResponse200]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = requests.get(
        verify=client.verify_ssl,
        auth=client.auth,
        timeout=client.timeout,
        **kwargs,
    )
    response.raise_for_status()

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[ControlledAccessTestRetrieveResponse200]:
    """View to determine whether you are authenticated with an account that has a specific
    role."""

    return sync_detailed(
        client=client,
    ).parsed


async def async_detailed(
    *,
    client: Client,
) -> Response[ControlledAccessTestRetrieveResponse200]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with client.get_async_session().get(
        verify_ssl=client.verify_ssl, raise_for_status=True, **kwargs
    ) as response:
        content = await response.read()
        resp = requests.Response()
        resp.status_code = response.status
        resp._content = content

    return _build_response(response=resp)


async def async_(
    *,
    client: Client,
) -> Optional[ControlledAccessTestRetrieveResponse200]:
    """View to determine whether you are authenticated with an account that has a specific
    role."""

    return (
        await async_detailed(
            client=client,
        )
    ).parsed
