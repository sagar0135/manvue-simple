# =========================================================
# Fashion Search & Classification (CLIP + FAISS + MongoDB)
# With: LR, RF, XGBoost, LightGBM, KNN, Decision Tree, SVM
# Rich visuals: Acc/F1 bars, Confusion Matrix, UMAP, PCA Corr
# =========================================================

# ---------- STEP 0: Install dependencies ----------
!pip -q install pymongo gridfs pillow transformers torch torchvision faiss-cpu datasets scikit-learn xgboost lightgbm matplotlib seaborn umap-learn

# ---------- STEP 1: Imports & Setup ----------
import os, io, json, datetime, warnings, math
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from PIL import Image

import torch
from transformers import CLIPProcessor, CLIPModel

from datasets import load_dataset
import faiss

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
from sklearn.decomposition import PCA

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

import umap
import matplotlib.pyplot as plt
import seaborn as sns

from pymongo import MongoClient
import gridfs

SEED = 42
np.random.seed(SEED)
torch.manual_seed(SEED)

# ---------- STEP 2: MongoDB connection ----------
# (Provided by you)
MONGO_URI = "mongodb+srv://19276146:19276146@manvue.ilich4r.mongodb.net/?retryWrites=true&w=majority&appName=MANVUE"
client = MongoClient(MONGO_URI)
db = client["MANVUE"]
fs = gridfs.GridFS(db)
print("✅ Connected to MongoDB MANVUE")

# ---------- STEP 3: Load CLIP ----------
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model_name = "openai/clip-vit-base-patch32"
clip_model = CLIPModel.from_pretrained(clip_model_name).to(device)
clip_processor = CLIPProcessor.from_pretrained(clip_model_name)
print(f"✅ Loaded CLIP on {device}")

# ---------- STEP 4: Load Fashion Dataset ----------
# Using HF dataset: ashraq/fashion-product-images-small (~44k); we'll use a subset for speed.
# Filter to Men only and cap size to keep Colab friendly.
MAX_ITEMS = 1500       # adjust up/down based on Colab runtime/RAM
SPLIT = f"train[:{MAX_ITEMS*2}]"  # load more, then filter to Men and keep <= MAX_ITEMS

ds = load_dataset("ashraq/fashion-product-images-small", split=SPLIT)
df = pd.DataFrame(ds)
# Keep "Men" only if available, else keep all
if "gender" in df.columns:
    df = df[df["gender"] == "Men"]
df = df.reset_index(drop=True)[:MAX_ITEMS]
print(f"✅ Loaded {len(df)} 'Men' items")

# ---------- STEP 5: Choose label & map to top-K classes ----------
# articleType is detailed but can be many classes. We'll take top-K frequent to make classification meaningful.
LABEL_COL = "articleType" if "articleType" in df.columns else "masterCategory"
TOP_K = 8
top_classes = df[LABEL_COL].value_counts().head(TOP_K).index.tolist()
df[LABEL_COL] = df[LABEL_COL].where(df[LABEL_COL].isin(top_classes), other="other")
print("Classes:", sorted(df[LABEL_COL].unique()))

# ---------- STEP 6: Build CLIP embeddings (image only) & save images/metadata to MongoDB ----------
def image_to_embedding(pil_img):
    inputs = clip_processor(images=[pil_img], return_tensors="pt").to(device)
    with torch.no_grad():
        feats = clip_model.get_image_features(**inputs)
    feats = feats / feats.norm(p=2, dim=-1, keepdim=True)
    return feats.cpu().numpy()[0].astype("float32")

embeddings = []
meta = []  # will store filename, label, name, color

for i, row in df.iterrows():
    try:
        # Convert HF bytes -> PIL
        img = Image.open(io.BytesIO(row["image"]["bytes"])).convert("RGB")
    except Exception as e:
        continue

    # Compute embedding
    emb = image_to_embedding(img)
    embeddings.append(emb)

    # Save image to MongoDB GridFS
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    filename = f"product_{i}.jpg"
    fs_id = fs.put(
        buf.read(),
        filename=filename,
        metadata={
            "name": row.get("productDisplayName", f"item_{i}"),
            "category": row.get("masterCategory", ""),
            "articleType": row.get("articleType", ""),
            "baseColour": row.get("baseColour", ""),
            "gender": row.get("gender", "")
        }
    )

    # Record metadata
    meta.append({
        "filename": filename,
        "name": row.get("productDisplayName", f"item_{i}"),
        "label": row.get(LABEL_COL, "other"),
        "category": row.get("masterCategory", ""),
        "articleType": row.get("articleType", ""),
        "baseColour": row.get("baseColour", ""),
        "gender": row.get("gender", "")
    })

    if (i+1) % 200 == 0:
        print(f"Processed {i+1} items...")

embeddings = np.vstack(embeddings).astype("float32")
meta_df = pd.DataFrame(meta)
print("✅ Embeddings shape:", embeddings.shape)

# Save metadata/index to local files (so you can reuse outside Colab if needed)
with open("metadata.json", "w") as f:
    json.dump(meta, f)

# ---------- STEP 7: Build FAISS index for similarity search ----------
dim = embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(dim)
faiss_index.add(embeddings)
faiss.write_index(faiss_index, "fashion.index")
print("✅ FAISS index built & saved")

# ---------- STEP 8: Prepare data for supervised models ----------
labels = meta_df["label"].values
le = LabelEncoder()
y = le.fit_transform(labels)   # numeric labels
X = embeddings                 # features are CLIP embeddings

X_train, X_test, y_train, y_test, meta_train, meta_test = train_test_split(
    X, y, meta_df, test_size=0.2, random_state=SEED, stratify=y
)

# ---------- STEP 9: Train multiple algorithms ----------
results = {}

def store_result(name, y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    f1m = f1_score(y_true, y_pred, average="macro", zero_division=0)
    results[name] = {"accuracy": acc, "f1_macro": f1m}
    print(f"{name:>16s}  |  Acc: {acc:.3f}  F1(macro): {f1m:.3f}")

print("\n⏳ Training models...")

# Logistic Regression
lr = LogisticRegression(max_iter=2000, n_jobs=None)
lr.fit(X_train, y_train)
store_result("Logistic Regression", y_test, lr.predict(X_test))

# Random Forest
rf = RandomForestClassifier(n_estimators=300, random_state=SEED, n_jobs=-1)
rf.fit(X_train, y_train)
store_result("Random Forest", y_test, rf.predict(X_test))

# XGBoost
xgb = XGBClassifier(
    n_estimators=400, max_depth=8, learning_rate=0.05, subsample=0.9, colsample_bytree=0.9,
    objective="multi:softmax", num_class=len(le.classes_), random_state=SEED, n_jobs=-1, tree_method="hist"
)
xgb.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
store_result("XGBoost", y_test, xgb.predict(X_test))

# LightGBM
lgbm = LGBMClassifier(
    n_estimators=500, learning_rate=0.05, subsample=0.9, colsample_bytree=0.9,
    random_state=SEED, n_jobs=-1
)
lgbm.fit(X_train, y_train)
store_result("LightGBM", y_test, lgbm.predict(X_test))

# KNN
knn = KNeighborsClassifier(n_neighbors=7, n_jobs=-1)
knn.fit(X_train, y_train)
store_result("KNN", y_test, knn.predict(X_test))

# Decision Tree
dt = DecisionTreeClassifier(max_depth=30, random_state=SEED)
dt.fit(X_train, y_train)
store_result("Decision Tree", y_test, dt.predict(X_test))

# SVM (linear for speed; switch to 'rbf' for potentially better but slower results)
svm = SVC(kernel="linear", probability=False, random_state=SEED)
svm.fit(X_train, y_train)
store_result("SVM", y_test, svm.predict(X_test))

print("\n✅ Training complete.")

# ---------- STEP 10: Visuals – Accuracy/F1 bar chart ----------
metrics_df = pd.DataFrame(results).T.sort_values(by="f1_macro", ascending=False)
plt.figure(figsize=(10,6))
metrics_df[["accuracy", "f1_macro"]].plot(kind="bar")
plt.title("Model Comparison: Accuracy & Macro F1 (higher is better)")
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()

# ---------- STEP 11: Confusion Matrix for Best Model ----------
best_model_name = metrics_df.index[0]
best_model = {
    "Logistic Regression": lr,
    "Random Forest": rf,
    "XGBoost": xgb,
    "LightGBM": lgbm,
    "KNN": knn,
    "Decision Tree": dt,
    "SVM": svm
}[best_model_name]

y_pred_best = best_model.predict(X_test)
cm = confusion_matrix(y_test, y_pred_best)
labels_order = le.inverse_transform(np.arange(len(le.classes_)))

plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=False, cmap="Blues", xticklabels=labels_order, yticklabels=labels_order, fmt="d")
plt.title(f"Confusion Matrix: {best_model_name}")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.tight_layout()
plt.show()

print(f"\n🎯 Best model: {best_model_name}")
print(classification_report(y_test, y_pred_best, target_names=labels_order, zero_division=0))

# ---------- STEP 12: UMAP 2D scatter of embeddings ----------
reducer = umap.UMAP(n_neighbors=20, min_dist=0.2, metric="cosine", random_state=SEED)
X_2d = reducer.fit_transform(X)
plt.figure(figsize=(8,7))
palette = sns.color_palette("husl", n_colors=len(le.classes_))
for idx, cls in enumerate(np.unique(y)):
    mask = y == cls
    plt.scatter(X_2d[mask,0], X_2d[mask,1], s=8, alpha=0.6, label=le.inverse_transform([cls])[0])
plt.legend(markerscale=2, bbox_to_anchor=(1.05, 1), loc="upper left")
plt.title("UMAP of CLIP Embeddings (colored by label)")
plt.tight_layout()
plt.show()

# ---------- STEP 13: PCA correlation heatmap (top 20 components) ----------
pca = PCA(n_components=20, random_state=SEED)
X_pca = pca.fit_transform(X)
corr = np.corrcoef(X_pca.T)
plt.figure(figsize=(8,6))
sns.heatmap(corr, cmap="coolwarm", center=0)
plt.title("Correlation Heatmap of Top 20 PCA Components")
plt.tight_layout()
plt.show()

# ---------- STEP 14: Similarity Search (CLIP + FAISS) ----------
def find_similar_from_path(image_path, top_k=6):
    img = Image.open(image_path).convert("RGB")
    emb = image_to_embedding(img).reshape(1, -1)
    D, I = faiss_index.search(emb, top_k)
    return meta_df.iloc[I[0]].to_dict(orient="records")

# ---------- STEP 15: Save models & metrics into MongoDB ----------
models_collection = db["models"]
record = {
    "timestamp": datetime.datetime.utcnow(),
    "clip_model": clip_model_name,
    "label_col": LABEL_COL,
    "classes": list(labels_order),
    "metrics": results
}
models_collection.insert_one(record)
print("✅ Stored model metrics in MongoDB collection 'models'")

# ---------- STEP 16: Log user upload + query results into MongoDB ----------
def upload_user_and_find(user_image_path, username="guest", top_k=6):
    # Save upload in GridFS
    with open(user_image_path, "rb") as f:
        img_bytes = f.read()
    upload_name = f"user_{username}_{int(datetime.datetime.utcnow().timestamp())}.jpg"
    file_id = fs.put(img_bytes, filename=upload_name, metadata={"username": username, "uploadedAt": datetime.datetime.utcnow()})

    # Find similar products
    results = find_similar_from_path(user_image_path, top_k=top_k)

    # Save query log
    db["queries"].insert_one({
        "username": username,
        "uploaded_file_id": str(file_id),
        "uploaded_filename": upload_name,
        "results": results,
        "createdAt": datetime.datetime.utcnow()
    })
    return results

print("\n💡 Ready! Use `upload_user_and_find('/content/your_image.jpg', 'alice')` to test.")

# ---------- OPTIONAL QUICK TEST ----------
# 1) Upload an image via Colab sidebar (Files) and set its path below to test:
# test_results = upload_user_and_find("/content/sample_fashion.jpg", username="alice")
# test_results[:3]
