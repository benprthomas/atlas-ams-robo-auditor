import { Request, Response } from "express";
import path from "path";
import { callAzureModel } from "../services/azureService";

export const processDocument = async (req: Request, res: Response) => {
  if (!req.file) {
    return res.status(400).send("PDF file is required");
  }

  const filePath = path.resolve(req.file.path);

  try {
    const result = await callAzureModel(filePath);
    res.status(200).json(result);
  } catch (error) {
    console.error("❌ Azure call failed:", error);
    res.status(500).send("Failed to process document");
  }
};
