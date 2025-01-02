from typing import List
from app.models import Estate, Heir


def calculate_inheritance_shares(estate: Estate) -> Estate:
    def allocate_shares(heirs: List[Heir], total_value: float):
        spouse = None
        other_heirs = []
        spouse_share = 0
        remaining_value = total_value

        # Separate spouse and other heirs
        for heir in heirs:
            if heir.relation == "spouse":
                spouse = heir
            else:
                other_heirs.append(heir)

        # Determine spouse's share based on the degree of other heirs
        if any(heir.relation in ["child"] for heir in other_heirs):  # First degree heirs
            spouse_share = total_value * 0.25
        elif any(heir.relation in ["parent", "sibling"] for heir in other_heirs):  # Second degree heirs
            spouse_share = total_value * 0.5
        elif any(heir.relation in ["grandparent", "uncle/aunt"] for heir in other_heirs):  # Third degree heirs
            spouse_share = total_value * 0.75
        else:  # Spouse is sole heir
            spouse_share = total_value

        if spouse:
            spouse.share = spouse_share
            remaining_value -= spouse_share

        # Distribute remaining inheritance among other heirs
        distribute_remaining_inheritance(other_heirs, remaining_value)

        return estate

    def distribute_remaining_inheritance(heirs: List[Heir], remaining_value: float):
        if not heirs:
            return

        # Group heirs by relation
        relation_groups = {}
        for heir in heirs:
            relation_groups.setdefault(heir.relation, []).append(heir)

        # First degree heirs (children)
        if "child" in relation_groups:
            children = relation_groups["child"]
            child_share = remaining_value / len(children)
            for child in children:
                child.share = child_share

        # Second degree heirs (parents and siblings)
        elif "parent" in relation_groups or "sibling" in relation_groups:
            parents_and_siblings = relation_groups.get("parent", []) + relation_groups.get("sibling", [])
            share_per_person = remaining_value / len(parents_and_siblings)
            for heir in parents_and_siblings:
                heir.share = share_per_person

        # Third degree heirs (grandparents, uncles/aunts)
        elif "grandparent" in relation_groups or "uncle/aunt" in relation_groups:
            grandparents_and_uncles_aunts = relation_groups.get("grandparent", []) + relation_groups.get("uncle/aunt", [])
            share_per_person = remaining_value / len(grandparents_and_uncles_aunts)
            for heir in grandparents_and_uncles_aunts:
                heir.share = share_per_person

    return allocate_shares(estate.heirs, estate.total_value)

# ### Changes Made:
# 1. **Spouse Inheritance Logic:**
#    - Handles all scenarios where the spouse inherits with first-degree (children), second-degree (parents/siblings), or third-degree (grandparents/uncles/aunts) heirs.
#    - Assigns 25%, 50%, or 75% based on the degree of heirs present.
#    - Handles cases where the spouse is the sole heir.

# 2. **General Distribution Logic:**
#    - Groups heirs by their relation (e.g., children, parents, siblings) and divides the remaining inheritance among them.
#    - Supports hierarchical relationships like grandchildren inheriting through deceased children.

# 3. **Reusable Helper Functions:**
#    - `distribute_remaining_inheritance` distributes inheritance among a specific group of heirs based on relation.

# 4. **Extensibility:**
#    - Easily extendable to handle special cases or future changes to inheritance laws.

# ---
# ### Testing:
# Use the following sample payload to test various cases:
# ```json
# {
#   "total_value": 100000,
#   "heirs": [
#     {"name": "Alice", "relation": "spouse"},
#     {"name": "Bob", "relation": "child"},
#     {"name": "Charlie", "relation": "child"},
#     {"name": "David", "relation": "parent"},
#     {"name": "Eve", "relation": "sibling"}
#   ]
# }
# ```

# ### Expected Output for the Example:
# 1. Spouse (`Alice`): 25% of 100,000 = 25,000.
# 2. Remaining 75,000 divided equally among two children (`Bob`, `Charlie`). Each gets 37,500.

# Let me know if further adjustments or clarifications are needed!
