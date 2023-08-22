from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.compound import Compound
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    mz_ratio: Union[Unset, None, float] = UNSET,
    database_list: Union[Unset, None, List[str]] = UNSET,
    polarity_list: Union[Unset, None, List[str]] = UNSET,
    mass_tolerance: Union[Unset, None, float] = UNSET,
    adducts: Union[Unset, None, List[str]] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["mz_ratio"] = mz_ratio

    json_database_list: Union[Unset, None, List[str]] = UNSET
    if not isinstance(database_list, Unset):
        if database_list is None:
            json_database_list = None
        else:
            json_database_list = database_list

    params["database_list"] = json_database_list

    json_polarity_list: Union[Unset, None, List[str]] = UNSET
    if not isinstance(polarity_list, Unset):
        if polarity_list is None:
            json_polarity_list = None
        else:
            json_polarity_list = polarity_list

    params["polarity_list"] = json_polarity_list

    params["mass_tolerance"] = mass_tolerance

    json_adducts: Union[Unset, None, List[str]] = UNSET
    if not isinstance(adducts, Unset):
        if adducts is None:
            json_adducts = None
        else:
            json_adducts = adducts

    params["adducts"] = json_adducts

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/compounds",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["Compound"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Compound.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["Compound"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    mz_ratio: Union[Unset, None, float] = UNSET,
    database_list: Union[Unset, None, List[str]] = UNSET,
    polarity_list: Union[Unset, None, List[str]] = UNSET,
    mass_tolerance: Union[Unset, None, float] = UNSET,
    adducts: Union[Unset, None, List[str]] = UNSET,
) -> Response[List["Compound"]]:
    """Returns all compounds from the system that the user has access to

    Args:
        mz_ratio (Union[Unset, None, float]):
        database_list (Union[Unset, None, List[str]]):
        polarity_list (Union[Unset, None, List[str]]):
        mass_tolerance (Union[Unset, None, float]):
        adducts (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['Compound']]
    """

    kwargs = _get_kwargs(
        mz_ratio=mz_ratio,
        database_list=database_list,
        polarity_list=polarity_list,
        mass_tolerance=mass_tolerance,
        adducts=adducts,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    mz_ratio: Union[Unset, None, float] = UNSET,
    database_list: Union[Unset, None, List[str]] = UNSET,
    polarity_list: Union[Unset, None, List[str]] = UNSET,
    mass_tolerance: Union[Unset, None, float] = UNSET,
    adducts: Union[Unset, None, List[str]] = UNSET,
) -> Optional[List["Compound"]]:
    """Returns all compounds from the system that the user has access to

    Args:
        mz_ratio (Union[Unset, None, float]):
        database_list (Union[Unset, None, List[str]]):
        polarity_list (Union[Unset, None, List[str]]):
        mass_tolerance (Union[Unset, None, float]):
        adducts (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['Compound']
    """

    return sync_detailed(
        client=client,
        mz_ratio=mz_ratio,
        database_list=database_list,
        polarity_list=polarity_list,
        mass_tolerance=mass_tolerance,
        adducts=adducts,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    mz_ratio: Union[Unset, None, float] = UNSET,
    database_list: Union[Unset, None, List[str]] = UNSET,
    polarity_list: Union[Unset, None, List[str]] = UNSET,
    mass_tolerance: Union[Unset, None, float] = UNSET,
    adducts: Union[Unset, None, List[str]] = UNSET,
) -> Response[List["Compound"]]:
    """Returns all compounds from the system that the user has access to

    Args:
        mz_ratio (Union[Unset, None, float]):
        database_list (Union[Unset, None, List[str]]):
        polarity_list (Union[Unset, None, List[str]]):
        mass_tolerance (Union[Unset, None, float]):
        adducts (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['Compound']]
    """

    kwargs = _get_kwargs(
        mz_ratio=mz_ratio,
        database_list=database_list,
        polarity_list=polarity_list,
        mass_tolerance=mass_tolerance,
        adducts=adducts,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    mz_ratio: Union[Unset, None, float] = UNSET,
    database_list: Union[Unset, None, List[str]] = UNSET,
    polarity_list: Union[Unset, None, List[str]] = UNSET,
    mass_tolerance: Union[Unset, None, float] = UNSET,
    adducts: Union[Unset, None, List[str]] = UNSET,
) -> Optional[List["Compound"]]:
    """Returns all compounds from the system that the user has access to

    Args:
        mz_ratio (Union[Unset, None, float]):
        database_list (Union[Unset, None, List[str]]):
        polarity_list (Union[Unset, None, List[str]]):
        mass_tolerance (Union[Unset, None, float]):
        adducts (Union[Unset, None, List[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['Compound']
    """

    return (
        await asyncio_detailed(
            client=client,
            mz_ratio=mz_ratio,
            database_list=database_list,
            polarity_list=polarity_list,
            mass_tolerance=mass_tolerance,
            adducts=adducts,
        )
    ).parsed
