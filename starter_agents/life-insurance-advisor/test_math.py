# test_math.py
# PURPOSE: Test coverage math with no API keys needed
# Run with: python test_math.py

from coverage import compute_local_breakdown, safe_number

print("Testing safe_number()...")
assert safe_number(None) == 0.0,        "❌ None should return 0"
assert safe_number("$85,000") == 85000, "❌ Should strip $ and comma"
assert safe_number(85000) == 85000.0,   "❌ Int should convert to float"
assert safe_number("abc") == 0.0,       "❌ Invalid string should return 0"
print("✅ safe_number() all tests passed")

print("\nTesting compute_local_breakdown()...")

# Standard profile
profile = {
    "annual_income": 85000,
    "income_replacement_years": 10,
    "total_debt": 200000,
    "available_savings": 50000,
    "existing_life_insurance": 100000
}

result = compute_local_breakdown(profile, real_rate=0.02)

print(f"\n📊 Calculation breakdown:")
print(f"  Annual income:          ${result['income']:,.0f}")
print(f"  Years:                  {result['years']}")
print(f"  Real rate:              {result['real_rate']*100:.1f}%")
print(f"  Annuity factor:         {result['annuity_factor']:.3f}")
print(f"  Discounted income:      ${result['discounted_income']:,.0f}")
print(f"  Total debt:             ${result['debt']:,.0f}")
print(f"  Assets offset:          ${result['assets_offset']:,.0f}")
print(f"  ✅ Recommended coverage: ${result['recommended']:,.0f}")

assert result['recommended'] > 0, "❌ Coverage should be positive"
assert result['annuity_factor'] > 0, "❌ Annuity factor should be positive"
assert result['discounted_income'] < 85000 * 10, "❌ Discounted should be less than simple sum"

print("\n✅ All math tests passed!")

# Edge case: zero rate
print("\nTesting edge case: zero discount rate...")
result_zero = compute_local_breakdown(profile, real_rate=0)
assert result_zero['discounted_income'] == 85000 * 10, "❌ Zero rate should give simple multiplication"
print("✅ Zero rate edge case passed!")

# Edge case: missing values
print("\nTesting edge case: missing profile values...")
empty_profile = {}
result_empty = compute_local_breakdown(empty_profile, real_rate=0.02)
assert result_empty['recommended'] == 0.0, "❌ Empty profile should give 0 coverage"
print("✅ Empty profile edge case passed!")

print("\n🎉 ALL TESTS PASSED — math.py is working correctly!")