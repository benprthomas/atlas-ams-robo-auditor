"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// keystone.ts
var keystone_exports = {};
__export(keystone_exports, {
  default: () => keystone_default
});
module.exports = __toCommonJS(keystone_exports);
var import_core2 = require("@keystone-6/core");

// schema.ts
var import_core = require("@keystone-6/core");
var import_fields = require("@keystone-6/core/fields");
var lists = {
  AutomationPlan: (0, import_core.list)({
    access: {
      operation: {
        query: () => true,
        create: () => true,
        update: () => true,
        delete: () => true
      }
    },
    fields: {
      title: (0, import_fields.text)({ validation: { isRequired: true } }),
      sourceDocumentUrl: (0, import_fields.text)(),
      extractedData: (0, import_fields.json)(),
      createdAt: (0, import_fields.timestamp)({ defaultValue: { kind: "now" } })
    }
  })
};

// keystone.ts
var dotenv = __toESM(require("dotenv"));
dotenv.config();
var keystone_default = (0, import_core2.config)({
  db: {
    provider: "postgresql",
    url: process.env.DATABASE_URL || ""
  },
  lists,
  server: {
    port: 3e3
  }
});
//# sourceMappingURL=config.js.map
