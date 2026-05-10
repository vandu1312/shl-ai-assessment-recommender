# =====================================
# BUILD CONTEXT
# =====================================

def build_context(messages):

    context = {
        "roles": set(),
        "technical": set(),
        "seniority": None,
        "personality": False,
        "stakeholder": False,
        "comparison": False,
        "unsafe": False,
    }

    full_text = " ".join(
        [msg["content"].lower() for msg in messages]
    )

    # =====================================
    # ROLE DETECTION
    # =====================================

    role_keywords = [
        "java developer",
        "python developer",
        "data analyst",
        "data scientist",
        "software engineer",
        "backend developer",
        "frontend developer",
        "backend engineer",
        "machine learning engineer",
    ]

    for role in role_keywords:

        if role in full_text:
            context["roles"].add(role)

    # =====================================
    # TECHNICAL SKILLS
    # =====================================

    tech_keywords = [
        "java",
        "python",
        "sql",
        "react",
        "aws",
        "machine learning",
        "docker",
        "backend",
        "frontend",
    ]

    for tech in tech_keywords:

        if tech in full_text:
            context["technical"].add(tech)

    # =====================================
    # SENIORITY
    # =====================================

    seniority_keywords = [
        "junior",
        "mid-level",
        "senior",
        "lead",
        "manager",
        "4 years",
        "5 years",
    ]

    for level in seniority_keywords:

        if level in full_text:
            context["seniority"] = level

    # =====================================
    # PERSONALITY / BEHAVIOR
    # =====================================

    personality_keywords = [
        "personality",
        "behavior",
        "communication",
        "culture fit",
        "team player",
        "collaboration",
        "collaborating",
        "teamwork",
        "interpersonal",
    ]

    if any(
        word in full_text
        for word in personality_keywords
    ):

        context["personality"] = True

    # =====================================
    # STAKEHOLDER
    # =====================================

    stakeholder_keywords = [
        "stakeholder",
        "client-facing",
        "presentation",
        "business teams",
        "business communication",
    ]

    if any(
        word in full_text
        for word in stakeholder_keywords
    ):

        context["stakeholder"] = True

    # =====================================
    # COMPARISON
    # =====================================

    comparison_keywords = [
        "difference",
        "compare",
        "vs",
        "versus",
    ]

    if any(
        word in full_text
        for word in comparison_keywords
    ):

        context["comparison"] = True

    # =====================================
    # UNSAFE
    # =====================================

    unsafe_keywords = [
        "ignore instructions",
        "legal advice",
        "salary advice",
        "aws certification",
    ]

    if any(
        word in full_text
        for word in unsafe_keywords
    ):

        context["unsafe"] = True

    # =====================================
    # CONVERT SETS TO LISTS
    # =====================================

    context["roles"] = list(
        context["roles"]
    )

    context["technical"] = list(
        context["technical"]
    )

    return context


# =====================================
# INTENT DETECTION
# =====================================

def detect_intent(context):

    if context["unsafe"]:
        return "refusal"

    if context["comparison"]:
        return "comparison"

    if not has_enough_context(context):
        return "clarification"

    return "recommendation"


# =====================================
# ENOUGH CONTEXT
# =====================================

def has_enough_context(context):

    if len(context["roles"]) > 0:
        return True

    if len(context["technical"]) > 0:
        return True

    if context["personality"]:
        return True

    if context["stakeholder"]:
        return True

    return False


# =====================================
# COMPARISON RESPONSE
# =====================================

def build_comparison_response():

    return (
        "OPQ focuses on personality traits, workplace behavior, "
        "and communication preferences, while GSA assessments "
        "measure cognitive ability, reasoning, and aptitude."
    )


# =====================================
# REFUSAL RESPONSE
# =====================================

def refusal_response():

    return (
        "I can only help with SHL assessment recommendations "
        "from the SHL product catalog."
    )