import ExcelJS from "exceljs";
import path from "path";
import fs from "fs";

export const generateExcel = async (data: any): Promise<string> => {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet("Adoption Agreement");

  // Example: Assume `data.fields` is a key-value map
  worksheet.columns = [
    { header: "Field", key: "field", width: 30 },
    { header: "Value", key: "value", width: 50 },
  ];

  Object.entries(data.fields).forEach(([key, value]) => {
    worksheet.addRow({ field: key, value });
  });

  const filePath = path.resolve(`backend/results/result-${Date.now()}.xlsx`);
  await workbook.xlsx.writeFile(filePath);

  return filePath;
};
