import fs from "fs";
import axios from "axios";
import path from "path";

const endpoint = process.env.AZURE_ENDPOINT;
const apiKey = process.env.AZURE_API_KEY;
const modelId = process.env.AZURE_MODEL_ID;
const apiVersion = process.env.AZURE_API_VERSION;
const DocumentIntelligence =
    require("@azure-rest/ai-document-intelligence").default,
  {
    getLongRunningPoller,
    isUnexpected,
  } = require("@azure-rest/ai-document-intelligence");

const { AzureKeyCredential } = require("@azure/core-auth");
const formUrl = `${endpoint}formrecognizer/documentModels/${modelId}:analyze?api-version=${apiVersion}`;

export const callAzureModel = async (pdfPath: string) => {
  const client = DocumentIntelligence(endpoint, new AzureKeyCredential(apiKey));

  const initialResponse = await client
    .path("/documentModels/{modelId}:analyze", "prebuilt-layout")
    .post({
      contentType: "application/json",
      body: {
        urlSource: formUrl,
      },
    });

  if (isUnexpected(initialResponse)) {
    throw initialResponse.body.error;
  }

  const poller = await getLongRunningPoller(client, initialResponse);
  const analyzeResult = (await poller.pollUntilDone()).body.analyzeResult;

  const documents = analyzeResult?.documents;

  const document = documents && documents[0];
  if (!document) {
    throw new Error("Expected at least one document in the result.");
  }

  console.log(
    "Extracted document:",
    document.docType,
    `(confidence: ${document.confidence || "<undefined>"})`
  );
  console.log("Fields:", document.fields);
};
