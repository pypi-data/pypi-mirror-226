from bittrade_huobi_websocket.models import RequestMessage, endpoints
from bittrade_huobi_websocket.rest.http_factory_decorator import http_factory


@http_factory
def query_deposit_address_http_factory(asset: str):
    return RequestMessage(
        "GET",
        endpoints.HuobiEndpoints.V2_DEPOSIT_ADDRESS,
        params={"currency": asset},
    )
