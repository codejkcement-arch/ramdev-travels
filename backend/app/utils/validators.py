import re
def clean_phone(phone: str | None):
    if not phone:
        return None
    value = re.sub(r"[^0-9+]", "", phone)
    if len(value.replace("+", "")) < 10:
        raise ValueError("Invalid phone number")
    return value
