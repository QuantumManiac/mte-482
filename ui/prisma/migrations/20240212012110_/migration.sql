/*
  Warnings:

  - You are about to drop the `CartItem` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropIndex
DROP INDEX "CartItem_productId_key";

-- DropTable
PRAGMA foreign_keys=off;
DROP TABLE "CartItem";
PRAGMA foreign_keys=on;

-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Product" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "price" REAL NOT NULL,
    "location" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "ingredients" TEXT,
    "imageUrl" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    "inCart" BOOLEAN NOT NULL DEFAULT false
);
INSERT INTO "new_Product" ("createdAt", "description", "id", "imageUrl", "ingredients", "location", "name", "price", "updatedAt") SELECT "createdAt", "description", "id", "imageUrl", "ingredients", "location", "name", "price", "updatedAt" FROM "Product";
DROP TABLE "Product";
ALTER TABLE "new_Product" RENAME TO "Product";
PRAGMA foreign_key_check;
PRAGMA foreign_keys=ON;
