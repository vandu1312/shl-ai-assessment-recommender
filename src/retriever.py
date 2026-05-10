import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# =====================================
# GLOBAL VARIABLES
# =====================================

model = None
df = None
catalog_embeddings = None


# =====================================
# LOAD MODEL LAZILY
# =====================================

def get_model():

    global model

    if model is None:

        model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )

    return model


# =====================================
# LOAD DATASET LAZILY
# =====================================

def load_catalog():

    global df
    global catalog_embeddings

    if df is None:

        df = pd.read_csv(
            "data/shl_assessments.csv"
        )

        df = df.fillna("")

        df = df.drop_duplicates(
            subset=["name"]
        )

        # =====================================
        # CREATE SEARCH TEXT
        # =====================================

        df["search_text"] = (
            df["name"].astype(str)
            + " "
            + df["test_type"].astype(str)
        )

        # =====================================
        # LIMIT DATASET SIZE
        # =====================================

        df = df.head(300)

        # =====================================
        # CREATE EMBEDDINGS ONLY ONCE
        # =====================================

        model_instance = get_model()

        catalog_embeddings = model_instance.encode(
            df["search_text"].tolist(),
            convert_to_numpy=True,
            show_progress_bar=False,
            batch_size=16
        )

    return df, catalog_embeddings


# =====================================
# RETRIEVE FUNCTION
# =====================================

def retrieve_assessments(context):

    model_instance = get_model()

    df_loaded, embeddings = load_catalog()

    query_parts = []

    query_parts.extend(
        context.get("roles", [])
    )

    query_parts.extend(
        context.get("technical", [])
    )

    if context.get("personality"):

        query_parts.append(
            "personality behavioral communication"
        )

    if context.get("stakeholder"):

        query_parts.append(
            "stakeholder communication teamwork"
        )

    query = " ".join(query_parts)

    if not query.strip():

        return []

    # =====================================
    # QUERY EMBEDDING
    # =====================================

    query_embedding = model_instance.encode(
        [query],
        convert_to_numpy=True,
        show_progress_bar=False
    )

    # =====================================
    # COSINE SIMILARITY
    # =====================================

    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    temp_df = df_loaded.copy()

    temp_df["score"] = similarities

    # =====================================
    # SORT RESULTS
    # =====================================

    results = (
        temp_df.sort_values(
            by="score",
            ascending=False
        )
        .head(10)
    )

    # =====================================
    # RETURN FORMAT
    # =====================================

    return results[
        ["name", "url", "test_type"]
    ].to_dict(orient="records")
