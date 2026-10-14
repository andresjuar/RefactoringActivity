"""Shipping quotation rules."""

DESTINATION_RATES = {
    "MX": (89.0, 18.0),
    "US": (199.0, 42.0),
}
DEFAULT_RATE = (299.0, 65.0)


def volumetric_weight(length_cm: float, width_cm: float, height_cm: float) -> float:
    return (length_cm * width_cm * height_cm) / 5000


def chargeable_weight(
    weight_kg: float,
    length_cm: float,
    width_cm: float,
    height_cm: float,
) -> float:
    volume_weight = volumetric_weight(length_cm, width_cm, height_cm)
    return max(weight_kg, volume_weight)


def shipping_quote(
    weight_kg: float,
    length_cm: float,
    width_cm: float,
    height_cm: float,
    destination_country: str,
    expedited: bool,
) -> float:
    billable = chargeable_weight(weight_kg, length_cm, width_cm, height_cm)

    base, per_kg = DESTINATION_RATES.get(destination_country, DEFAULT_RATE)

    total = base + billable * per_kg

    if expedited:
        total *= 1.35

    if any(dim > 100 for dim in (length_cm, width_cm, height_cm)):
        total += 120.0

    return round(total, 2)