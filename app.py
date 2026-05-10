import streamlit as st

from src.utils import (
    build_context,
    detect_intent,
    has_enough_context,
    build_comparison_response,
    refusal_response,
)

from src.retriever import retrieve_assessments


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="SHL AI Assessment Recommender",
    layout="wide"
)

# =====================================
# TITLE
# =====================================

st.title(
    "SHL AI Assessment Recommendation System"
)

st.markdown(
    """
    Enter hiring requirements, role details,
    technical skills, or behavioral needs
    to receive recommended SHL assessments.
    """
)

# =====================================
# INPUT
# =====================================

query = st.text_area(
    "Enter Hiring Requirement",
    placeholder=(
        "Example: Hiring Python developer "
        "with communication and teamwork skills"
    ),
    height=150
)

# =====================================
# BUTTON
# =====================================

if st.button("Get Recommendations"):

    if not query.strip():

        st.warning(
            "Please enter a hiring requirement."
        )

    else:

        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        # =====================================
        # BUILD CONTEXT
        # =====================================

        context = build_context(messages)

        # =====================================
        # DETECT INTENT
        # =====================================

        intent = detect_intent(context)

        # =====================================
        # REFUSAL
        # =====================================

        if intent == "refusal":

            st.error(
                refusal_response()
            )

        # =====================================
        # COMPARISON
        # =====================================

        elif intent == "comparison":

            st.info(
                build_comparison_response()
            )

        # =====================================
        # CLARIFICATION
        # =====================================

        elif not has_enough_context(context):

            st.warning(
                "Could you share more details "
                "about the role, skills, "
                "or seniority level?"
            )

        # =====================================
        # RETRIEVAL
        # =====================================

        else:

            recommendations = retrieve_assessments(
                context
            )

            # =====================================
            # NO RESULTS
            # =====================================

            if len(recommendations) == 0:

                st.warning(
                    "No matching SHL assessments found."
                )

            # =====================================
            # DISPLAY RESULTS
            # =====================================

            else:

                st.success(
                    f"Found {len(recommendations)} matching assessments"
                )

                for rec in recommendations:

                    with st.container():

                        st.markdown(
                            f"## {rec['name']}"
                        )

                        st.write(
                            f"Assessment Type: {rec['test_type']}"
                        )

                        st.markdown(
                            f"[Open Assessment]({rec['url']})"
                        )

                        st.divider()
