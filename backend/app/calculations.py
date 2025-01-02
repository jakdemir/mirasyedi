from app.models import Estate, Heir

def calculate_inheritance_shares(estate: Estate) -> Estate:
    # Example rules:
    # - Spouse gets 50% if children exist; otherwise, gets 75%.
    # - Children equally share the remainder.
    # - If no children, parents and siblings share based on specific ratios.
    
    total_value = estate.total_value
    heirs = estate.heirs

    spouse = next((heir for heir in heirs if heir.relation == "spouse"), None)
    children = [heir for heir in heirs if heir.relation == "child"]

    if spouse:
        if children:
            spouse.share = total_value * 0.5
            remaining_value = total_value * 0.5
        else:
            spouse.share = total_value * 0.75
            remaining_value = total_value * 0.25
    else:
        remaining_value = total_value

    if children:
        for child in children:
            child.share = remaining_value / len(children)
    else:
        # Additional logic for parents, siblings, etc.
        pass

    return estate
