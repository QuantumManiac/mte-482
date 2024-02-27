-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Product" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "price" REAL NOT NULL,
    "location" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "ingredients" TEXT,
    "image" TEXT NOT NULL DEFAULT 'placeholder.jpg',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    "inCart" BOOLEAN NOT NULL DEFAULT false,
    "rfid" TEXT
);
INSERT INTO "new_Product" ("createdAt", "description", "id", "image", "inCart", "ingredients", "location", "name", "price", "rfid", "updatedAt") SELECT "createdAt", "description", "id", coalesce("image", 'placeholder.jpg') AS "image", "inCart", "ingredients", "location", "name", "price", "rfid", "updatedAt" FROM "Product";
DROP TABLE "Product";
ALTER TABLE "new_Product" RENAME TO "Product";
PRAGMA foreign_key_check;
PRAGMA foreign_keys=ON;
