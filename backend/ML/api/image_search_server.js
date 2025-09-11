import express from "express";
import multer from "multer";
import { MongoClient, GridFSBucket } from "mongodb";
import { spawn } from "child_process";
import path from "path";

const app = express();
const port = 3000;
const upload = multer({ storage: multer.memoryStorage() });

const url = "mongodb+srv://19276146:19276146@manvue.ilich4r.mongodb.net/?retryWrites=true&w=majority&appName=MANVUE";
const dbName = "MANVUE";

let db, bucket;

// Connect to MongoDB
MongoClient.connect(url).then(client => {
  db = client.db(dbName);
  bucket = new GridFSBucket(db, { bucketName: "images" });
  console.log("✅ Connected to MongoDB Atlas");
});

// Serve static frontend
app.use(express.static("public"));

// API: Upload image + run CLIP + FAISS (via Python)
app.post("/upload", upload.single("image"), async (req, res) => {
  try {
    const filename = Date.now() + "_" + req.file.originalname;

    // Save uploaded file in GridFS
    const uploadStream = bucket.openUploadStream(filename, {
      metadata: { uploadedBy: "user1", category: "unknown" }
    });
    uploadStream.end(req.file.buffer);

    // Call Python script to run CLIP + FAISS
    const py = spawn("python3", ["search.py", filename]);

    let data = "";
    py.stdout.on("data", chunk => (data += chunk.toString()));
    py.on("close", () => {
      try {
        res.json(JSON.parse(data));
      } catch (err) {
        res.status(500).json({ error: "Python returned invalid response" });
      }
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Serve images from MongoDB
app.get("/image/:filename", (req, res) => {
  bucket.openDownloadStreamByName(req.params.filename)
    .on("error", () => res.status(404).send("Image not found"))
    .pipe(res);
});

app.listen(port, () => console.log(`🚀 Server running at http://localhost:${port}`));
