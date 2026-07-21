from decimal import Decimal, ROUND_HALF_UP

def fmt_price(price: float, digits: int):
    return f"{price:.{digits}f}"

def to_decimal(price: float, digits: int):
    quant = Decimal(1).scaleb(-digits)
    return Decimal(str(price)).quantize(quant, rounding=ROUND_HALF_UP)