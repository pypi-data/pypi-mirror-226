from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.compound import Compound
from ...models.new_compound import NewCompound
from ...types import UNSET, Response


def _get_kwargs(
    *,
    compound: "NewCompound",
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_compound = compound.to_dict()

    params.update(json_compound)

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": "/compounds",
        "params": params,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Compound]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = Compound.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Compound]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    compound: "NewCompound",
) -> Response[Compound]:
    """Creates a new compound in the database. Duplicates are not allowed

    Args:
        compound (NewCompound):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Compound]
    """

    kwargs = _get_kwargs(
        compound=compound,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    compound: "NewCompound",
) -> Optional[Compound]:
    """Creates a new compound in the database. Duplicates are not allowed

    Args:
        compound (NewCompound):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Compound
    """

    return sync_detailed(
        client=client,
        compound=compound,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    compound: "NewCompound",
) -> Response[Compound]:
    """Creates a new compound in the database. Duplicates are not allowed

    Args:
        compound (NewCompound):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Compound]
    """

    kwargs = _get_kwargs(
        compound=compound,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    compound: "NewCompound",
) -> Optional[Compound]:
    """Creates a new compound in the database. Duplicates are not allowed

    Args:
        compound (NewCompound):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Compound
    """

    return (
        await asyncio_detailed(
            client=client,
            compound=compound,
        )
    ).parsed
