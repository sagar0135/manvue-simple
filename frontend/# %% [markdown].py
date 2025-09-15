# %% [markdown]
# # Fashion Product Dataset MongoDB Loader
# 
# This notebook loads an already-extracted Fashion Product dataset into MongoDB.
# 
# ## Dataset Structure
# 
# ```
# <ROOT_DIR>/
#   ├─ data.csv           <-- metadata CSV
#   └─ data/              <-- folder that contains all images (jpg/png/webp)
# ```
# 
# ## What it does
# - Loads `<ROOT_DIR>/data.csv`
# - Maps image filenames/paths from the CSV to files inside `<ROOT_DIR>/data/`
# - Inserts documents into MongoDB
# 
# ## Setup
# ```bash
# pip install pandas pymongo gridfs
# ```
# 

# %%
# Import required libraries
from __future__ import annotations

import os
import sys
import json
from pathlib import Path
from typing import Optional, Iterable, List, Dict
from collections import defaultdict

import pandas as pd
from pymongo import MongoClient, ASCENDING
import gridfs


# %% [markdown]
# ## Configuration
# 
# Edit these variables according to your setup:
# 

# %%
# ========== CONFIG (edit these) ==========
ROOT_DIR = Path(r"C:\Users\rushi\Desktop\technical-test")   # <-- change to your folder containing data.csv and data/
CSV_NAME = "data.csv"
IMAGES_DIRNAME = "data"                      # the folder that has images
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "fashion_db")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "products")
GRIDFS_BUCKET = os.getenv("MONGO_GRIDFS_BUCKET", "fs")

STORE_IMAGES_IN_GRIDFS = bool(int(os.getenv("STORE_IMAGES_IN_GRIDFS", "0")))  # 0=no, 1=yes
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))
# =========================================

print("Configuration:")
print(f"  ROOT_DIR: {ROOT_DIR}")
print(f"  CSV_NAME: {CSV_NAME}")
print(f"  IMAGES_DIRNAME: {IMAGES_DIRNAME}")
print(f"  MONGO_URI: {MONGO_URI}")
print(f"  DB_NAME: {DB_NAME}")
print(f"  COLLECTION_NAME: {COLLECTION_NAME}")
print(f"  STORE_IMAGES_IN_GRIDFS: {STORE_IMAGES_IN_GRIDFS}")
print(f"  BATCH_SIZE: {BATCH_SIZE}")


# %% [markdown]
# ## Utility Functions
# 

# %%
def die(msg: str, code: int = 1):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(code)


def pick_col(df: pd.DataFrame, candidates: Iterable[str]) -> Optional[str]:
    """Find a column name that matches any of the candidate strings (case-insensitive)"""
    for name in df.columns:
        low = name.lower()
        if any(key in low for key in candidates):
            return name
    return None


def infer_columns(df: pd.DataFrame):
    """Automatically infer column names for common fields"""
    col_id = pick_col(df, {"id", "product_id", "sku"})
    col_title = pick_col(df, {"title", "name", "product_title"})
    col_desc = pick_col(df, {"description", "desc", "product_description", "text"})
    col_image = pick_col(df, {"image", "image_path", "img", "filename", "file", "image_name", "image_url"})
    
    print("[INFO] Inferred columns:")
    print("  id      :", col_id)
    print("  title   :", col_title)
    print("  desc    :", col_desc)
    print("  image   :", col_image)
    return col_id, col_title, col_desc, col_image


# %% [markdown]
# ## Image Processing Functions
# 

# %%
def build_image_lookup(images_root: Path) -> Dict[str, List[Path]]:
    """
    Build a lookup so we can resolve an image by:
      - its basename (e.g., '12345.jpg')
      - its stem without extension (e.g., '12345')
    We scan only under <ROOT_DIR>/data/.
    """
    if not images_root.exists():
        die(f"Images folder not found: {images_root}")

    lookup: Dict[str, List[Path]] = defaultdict(list)
    for p in images_root.rglob("*"):
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
            lookup[p.name].append(p)
            lookup[p.stem].append(p)
    
    print(f"[INFO] Indexed {sum(len(v) for v in lookup.values())} image entries from {images_root}")
    return lookup


def resolve_image_path(value, images_root: Path, image_lookup: Dict[str, List[Path]]) -> Optional[str]:
    """Resolve image path from various formats (filename, path, etc.)"""
    if pd.isna(value):
        return None
    s = str(value).strip()

    # Try by basename
    base = Path(s).name
    if base in image_lookup:
        return str(image_lookup[base][0])

    # Try by stem (without extension)
    stem = Path(s).stem
    if stem in image_lookup:
        return str(image_lookup[stem][0])

    # Try as direct path
    candidate = images_root / s
    if candidate.exists():
        return str(candidate.resolve())

    return None


def content_type_for_suffix(suffix: str) -> str:
    """Get MIME type for image file extension"""
    s = suffix.lower()
    if s == ".png":
        return "image/png"
    if s == ".webp":
        return "image/webp"
    return "image/jpeg"


# %% [markdown]
# ## Data Processing Functions
# 

# %%
def normalize_records(
    df: pd.DataFrame,
    images_root: Path,
    image_lookup: Dict[str, List[Path]],
    col_id: Optional[str],
    col_title: Optional[str],
    col_desc: Optional[str],
    col_image: Optional[str],
) -> List[dict]:
    """Convert DataFrame rows to normalized MongoDB documents"""
    records: List[dict] = []
    for _, row in df.iterrows():
        rec: dict = {}

        # Map columns to standard field names
        if col_id and pd.notna(row.get(col_id, None)):
            rec["product_id"] = str(row[col_id])
        if col_title and pd.notna(row.get(col_title, None)):
            rec["title"] = str(row[col_title])
        if col_desc and pd.notna(row.get(col_desc, None)):
            rec["description"] = str(row[col_desc])

        # Resolve image path
        img_ref = None
        if col_image and col_image in df.columns:
            img_ref = resolve_image_path(row[col_image], images_root, image_lookup)
        else:
            # fallback: try to infer from product_id or title
            for key in [row.get(col_id, None), row.get(col_title, None)]:
                if pd.notna(key):
                    candidate = resolve_image_path(key, images_root, image_lookup)
                    if candidate:
                        img_ref = candidate
                        break

        if img_ref:
            rec["image_path"] = img_ref
            rec["image_filename"] = Path(img_ref).name

        # keep original row in case you need extra fields later
        rec["raw"] = {k: (None if pd.isna(v) else v) for k, v in row.items()}
        records.append(rec)

    print(f"[INFO] Prepared {len(records)} normalized records")
    return records


# %% [markdown]
# ## MongoDB Functions
# 

# %%
def connect_mongo(uri: str, db_name: str, coll_name: str, gridfs_bucket: str):
    """Connect to MongoDB and create necessary indexes"""
    client = MongoClient(uri)
    db = client[db_name]
    coll = db[coll_name]
    fs = gridfs.GridFS(db, collection=gridfs_bucket)

    # helpful indexes (sparse, not unique by default)
    try:
        coll.create_index([("product_id", ASCENDING)], sparse=True)
        coll.create_index([("image_filename", ASCENDING)], sparse=True)
        coll.create_index([("title", ASCENDING)], sparse=True)
    except Exception as e:
        print("[WARN] Index creation issue:", e)

    print(f"[INFO] Mongo connected → {db_name}.{coll_name} (docs: {coll.estimated_document_count()})")
    return client, db, coll, fs


def put_image_to_gridfs(fs: gridfs.GridFS, path_str: str):
    """Store image file in GridFS"""
    p = Path(path_str)
    if not p.exists():
        return None
    with open(p, "rb") as f:
        data = f.read()
    return fs.put(
        data,
        filename=p.name,
        contentType=content_type_for_suffix(p.suffix),
        metadata={"source_path": str(p.resolve())},
    )


def insert_batched(coll, docs: List[dict], batch_size: int) -> tuple[int, int]:
    """Insert documents in batches for better performance"""
    inserted, skipped = 0, 0
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i+batch_size]
        try:
            res = coll.insert_many(batch, ordered=False)
            inserted += len(res.inserted_ids)
        except Exception as e:
            print(f"[WARN] Batch insert issue ({e}); trying per-document for this batch.")
            for d in batch:
                try:
                    coll.insert_one(d)
                    inserted += 1
                except Exception:
                    skipped += 1
    return inserted, skipped


# %% [markdown]
# ## Main Execution
# 
# Now let's run the main process to load the data into MongoDB:
# 

# %%
# Step 1: Validate paths and load CSV
csv_path = ROOT_DIR / CSV_NAME
images_root = ROOT_DIR / IMAGES_DIRNAME

if not csv_path.exists():
    die(f"CSV not found: {csv_path}")
if not images_root.exists():
    die(f"Images folder not found: {images_root}")

print("[INFO] Loading CSV:", csv_path)
df = pd.read_csv(csv_path, low_memory=False)
print("[INFO] CSV columns:", list(df.columns))
print(f"[INFO] CSV shape: {df.shape}")
print(f"[INFO] First few rows:")
df.head()


# %%
# Step 2: Infer columns and build image lookup
col_id, col_title, col_desc, col_image = infer_columns(df)
image_lookup = build_image_lookup(images_root)


# %%
# Step 3: Normalize records
records = normalize_records(df, images_root, image_lookup, col_id, col_title, col_desc, col_image)

# Show sample of normalized records
print("\n[INFO] Sample normalized records:")
for i, record in enumerate(records[:3]):
    print(f"Record {i+1}:")
    print(json.dumps(record, default=str, indent=2))
    print("-" * 50)


# %%
# Step 4: Connect to MongoDB
client, db, coll, fs = connect_mongo(MONGO_URI, DB_NAME, COLLECTION_NAME, GRIDFS_BUCKET)


# %%
# Step 5: Store images in GridFS (if enabled)
if STORE_IMAGES_IN_GRIDFS:
    print("[INFO] Storing images in GridFS …")
    for rec in records:
        img_path = rec.get("image_path")
        if img_path:
            try:
                file_id = put_image_to_gridfs(fs, img_path)
                if file_id:
                    rec["image_file_id"] = file_id
            except Exception as e:
                print(f"[WARN] GridFS store failed for {img_path}: {e}")
else:
    print("[INFO] Skipping GridFS storage (STORE_IMAGES_IN_GRIDFS=False)")


# %%
# Step 6: Insert documents into MongoDB
print("[INFO] Inserting documents …")
inserted, skipped = insert_batched(coll, records, BATCH_SIZE)
print(f"[DONE] Inserted: {inserted}, Skipped: {skipped}")
print(f"[INFO] Collection now has {coll.estimated_document_count()} documents.")


# %%
# Step 7: Show sample document from database
sample = coll.find_one({}, projection={"raw": False})
print("[SAMPLE DOC]")
print(json.dumps(sample, default=str, indent=2))


# %% [markdown]
# ## Summary
# 
# The notebook has successfully:
# 1. ✅ Loaded the CSV data
# 2. ✅ Built an image lookup index
# 3. ✅ Normalized records for MongoDB
# 4. ✅ Connected to MongoDB
# 5. ✅ Stored images in GridFS (if enabled)
# 6. ✅ Inserted documents in batches
# 7. ✅ Displayed sample results
# 
# ## Next Steps
# 
# You can now:
# - Query the MongoDB collection for specific products
# - Use the GridFS file IDs to retrieve images
# - Build APIs on top of this data
# - Perform analytics on the fashion product dataset
# 


