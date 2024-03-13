/*
  Warnings:

  - You are about to drop the column `location` on the `Product` table. All the data in the column will be lost.

*/
-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Product" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "price" REAL NOT NULL,
    "locationText" TEXT,
    "locationX" REAL,
    "locationY" REAL,
    "description" TEXT NOT NULL,
    "additionalInfo" TEXT,
    "image" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    "inCart" BOOLEAN NOT NULL DEFAULT false,
    "done" BOOLEAN NOT NULL DEFAULT false,
    "rfid" TEXT
);
INSERT INTO "new_Product" ("additionalInfo", "createdAt", "description", "done", "id", "image", "inCart", "name", "price", "rfid", "updatedAt") SELECT "additionalInfo", "createdAt", "description", "done", "id", "image", "inCart", "name", "price", "rfid", "updatedAt" FROM "Product";
DROP TABLE "Product";
ALTER TABLE "new_Product" RENAME TO "Product";
PRAGMA foreign_key_check;
PRAGMA foreign_keys=ON;
