from mini_store.pricing import calculate_order_total


def test_standard_customer_in_mexico_pays_tax_and_shipping():
    assert calculate_order_total(500, "standard", None, "MX") == 679.0


def test_premium_customer_receives_discount():
    assert calculate_order_total(1000, "premium", None, "MX") == 1143.0


def test_save20_coupon_requires_minimum_subtotal():
    assert calculate_order_total(1400, "standard", "SAVE20", "MX") == 1624.0


def test_employee_and_save5_coupon_in_us():
    assert calculate_order_total(100, "employee", "SAVE5", "US") == 379.0

def test_save20_coupon_applied_and_us_discounted_shipping():
    assert calculate_order_total(3000, "standard", "SAVE20", "US") == 2599.0

def test_discount_exceeds_subtotal_forces_zero():
    assert calculate_order_total(0, "employee", "SAVE5", "MX") == 99.0