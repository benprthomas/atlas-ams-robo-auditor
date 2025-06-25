import { config } from "@keystone-6/core";
import { lists } from "./schema";
import * as dotenv from "dotenv";
dotenv.config();

export default config({
  db: {
    provider: "postgresql",
    url: process.env.DATABASE_URL || "",
  },
  lists,
  server: {
    port: 3000,
  },
});
