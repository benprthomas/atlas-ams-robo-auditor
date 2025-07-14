import express from "express";
import multer from "multer";
import cors from "cors";
import dotenv from "dotenv";
import { processDocument } from "./controllers/processor";

dotenv.config();
const app = express();
const port = process.env.PORT || 5000;

const upload = multer({ dest: "backend/uploads/" });

app.use(cors());
app.use(express.json());

app.post("/api/upload", upload.single("pdf"), processDocument);

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
