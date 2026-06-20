# math.py
# PURPOSE: Pure coverage math — no AI, no API, just calculations
# This can always be tested without any internet or API keys


def compute_local_breakdown(profile: dict, real_rate: float) -> dict:
    """
    Calculates how much life insurance coverage someone needs.

    Formula:
    coverage = discounted_income + total_debt - savings - existing_cover

    Args:
        profile: dict with user financial details
        real_rate: discount rate as decimal e.g. 0.02 for 2%

    Returns:
        dict with all calculation steps
    """

    # Step 1: Extract values from profile
    # if value is missing, treat as 0
    income = safe_number(profile.get("annual_income"))
    years = max(0, int(profile.get("income_replacement_years", 0) or 0))
    total_debt = safe_number(profile.get("total_debt"))
    savings = safe_number(profile.get("available_savings"))
    existing_cover = safe_number(profile.get("existing_life_insurance"))

    # Step 2: Calculate annuity factor
    # This is how much $1/year is worth over N years at rate r
    # Example: $85000/year for 10 years at 2% is NOT just $850000
    # because future money is worth less than today's money
    if real_rate <= 0:
        annuity_factor = years
        discounted_income = income * years
    else:
        annuity_factor = (1 - (1 + real_rate) ** (-years)) / real_rate
        discounted_income = income * annuity_factor

    # Step 3: Calculate assets that reduce coverage needed
    assets_offset = savings + existing_cover

    # Step 4: Final recommended coverage
    # can never be negative
    recommended = max(0.0, discounted_income + total_debt - assets_offset)

    # Step 5: Return ALL steps so UI can show the math
    return {
        "income": income,
        "years": years,
        "real_rate": real_rate,
        "annuity_factor": annuity_factor,
        "discounted_income": discounted_income,
        "debt": total_debt,
        "assets_offset": -assets_offset,   # negative because it reduces coverage
        "recommended": recommended,
    }


def safe_number(value) -> float:
    """
    Safely converts any value to float.
    Returns 0.0 if conversion fails.
    """
    if value is None:
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        if isinstance(value, str):
            # Remove currency symbols and commas
            cleaned = value
            for symbol in [",", "$", "€", "£", "₹", "C$", "A$"]:
                cleaned = cleaned.replace(symbol, "")
            try:
                return float(cleaned.strip())
            except ValueError:
                return 0.0
        return 0.0