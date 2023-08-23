from enum import Enum


class Endpoints(Enum):
    """Enum class for all the endpoints"""

    GET_RECEIVE_ADDRESS = "/api/1/funding_address"
    GET_BALANCES = "/api/1/balance"
    GET_ORDER_V3 = "/api/exchange/3/order"
    GET_FEE_INFORMATION = "/api/1/fee_info"
    POST_MARKET_ORDER = "/api/1/marketorder"
    POST_LIMIT_ORDER = "/api/1/postorder"
    ORDERBOOK_TOP = "/api/1/orderbook_top"
