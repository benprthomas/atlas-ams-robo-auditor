import { list } from "@keystone-6/core";
import { text, json, timestamp } from "@keystone-6/core/fields";

export const lists = {
  AutomationPlan: list({
    access: {
      operation: {
        query: () => true,
        create: () => true,
        update: () => true,
        delete: () => true,
      },
    },
    fields: {
      title: text({ validation: { isRequired: true } }),
      sourceDocumentUrl: text(),
      extractedData: json(),
      createdAt: timestamp({ defaultValue: { kind: "now" } }),
    },
  }),
};
