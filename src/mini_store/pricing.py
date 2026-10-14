"""Pricing rules for orders."""


def _calculate_discount(subtotal: float, customer_type: str, coupon_code: str | None) -> float:
    """Calcula el descuento total basado en el tipo de cliente y cupones."""
    discount = 0.0
    if customer_type == "premium":
        discount = subtotal * 0.10
    elif customer_type == "employee":
        discount = subtotal * 0.15

    if coupon_code == "SAVE5":
        discount += subtotal * 0.05
    elif coupon_code == "SAVE20" and subtotal >= 1500:
        discount += subtotal * 0.20
        
    return discount

def _calculate_tax(amount: float, country: str) -> float:
    """Calcula los impuestos aplicables según el país."""
    return amount * 0.16 if country == "MX" else 0.0

def _calculate_shipping(amount: float, country: str) -> float:
    """Calcula la tarifa de envío según el país y el monto de compra."""
    if country == "MX":
        return 0.0 if amount >= 1000 else 99.0
    else:
        return 199.0 if amount >= 2000 else 299.0
def calculate_order_total(
    subtotal: float,
    customer_type: str,
    coupon_code: str | None,
    country: str,
) -> float:
    """Return the final order total after discounts, tax, and shipping."""
 
    # 1. Aplicar descuentos
    discount = _calculate_discount(subtotal, customer_type, coupon_code)
    discounted_subtotal = max(0.0, subtotal - discount)
    
    # 2. Calcular impuestos y envío
    tax = _calculate_tax(discounted_subtotal, country)
    shipping = _calculate_shipping(discounted_subtotal, country)

    # 3. Retornar total
    return round(discounted_subtotal + tax + shipping, 2)
