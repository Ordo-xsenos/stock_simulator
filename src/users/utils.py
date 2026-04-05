def format_currency(amount: float, currency: str = "USD") -> str:
    """Форматирует число в строку с валютой."""
    return f"{amount:,.2f} {currency}"


def calculate_percentage_change(old_price: float, new_price: float) -> float:
    """Вычисляет процентное изменение между двумя значениями."""
    if old_price == 0:
        return 0.0
    return ((new_price - old_price) / old_price) * 100

def format_percentage_change(percentage: float) -> str:
    """Форматирует процентное изменение в строку с плюсом или минусом."""
    sign = "+" if percentage >= 0 else "-"
    return f"{sign}{abs(percentage):.2f}%"


def format_price_change(old_price: float, new_price: float, currency: str = "USD") -> str:
    """Форматирует изменение цены в строку с валютой и процентами."""
    percentage_change = calculate_percentage_change(old_price, new_price)
    formatted_percentage = format_percentage_change(percentage_change)
    formatted_new_price = format_currency(new_price, currency)
    return f"{formatted_new_price} ({formatted_percentage})"


def is_market_open(current_time: str) -> bool:
    """Проверяет, открыт ли рынок в заданное время (формат HH:MM)."""
    from datetime import datetime, time

    market_open_time = time(9, 30)  # 9:30 AM
    market_close_time = time(16, 0)   # 4:00 PM

    try:
        current_time_obj = datetime.strptime(current_time, "%H:%M").time()
        return market_open_time <= current_time_obj <= market_close_time
    except ValueError:
        raise ValueError("Invalid time format. Expected HH:MM.")