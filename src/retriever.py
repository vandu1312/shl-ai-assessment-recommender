
import os
import pandas as pd
import gc

from sklearn.metrics.pairwise import cosine_similarity


# =====================================
# GLOBAL VARIABLES
# =====================================

model = None
df = None
catalog_embeddings = None

# Resolve dataset path independently of working directory
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "shl_assessments.csv"
)


# =====================================
# LOAD MODEL LAZILY
# =====================================

def get_model():

    global model

    if model is None:

        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
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

        if not os.path.exists(DATASET_PATH):
            raise FileNotFoundError(
                f"Dataset not found: {DATASET_PATH}"
            )

        df = pd.read_csv(DATASET_PATH)

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

        df = df.head(300).reset_index(drop=True)

        # =====================================
        # CREATE EMBEDDINGS ONLY ONCE
        # =====================================

        model_instance = get_model()

        catalog_embeddings = model_instance.encode(
            df["search_text"].tolist(),
            convert_to_numpy=True,
            show_progress_bar=False,
            batch_size=4
        )

        gc.collect()

    return df, catalog_embeddings


# =====================================
# RETRIEVE FUNCTION
# =====================================

def retrieve_assessments(context):

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
    # LOAD MODEL AND CATALOG
    # =====================================

    model_instance = get_model()

    df_loaded, embeddings = load_catalog()

    # =====================================
    # QUERY EMBEDDING
    # =====================================

    query_embedding = model_instance.encode(
        [query],
        convert_to_numpy=True,
        show_progress_bar=False,
        batch_size=1
    )

    # =====================================
    # COSINE SIMILARITY
    # =====================================

    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    # =====================================
    # SORT RESULTS
    # =====================================

    top_indices = similarities.argsort()[::-1][:10]

    results = df_loaded.iloc[top_indices]

    # =====================================
    # RETURN FORMAT
    # =====================================

    return results[
        ["name", "url", "test_type"]
    ].to_dict(orient="records")
