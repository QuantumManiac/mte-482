/*
  Warnings:

  - You are about to drop the column `destinationName` on the `NavigationState` table. All the data in the column will be lost.
  - You are about to drop the column `routeTo` on the `NavigationState` table. All the data in the column will be lost.

*/
-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_NavigationState" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT DEFAULT 0,
    "state" TEXT NOT NULL DEFAULT 'idle',
    "destX" REAL,
    "destY" REAL,
    "destName" TEXT,
    "route" TEXT,
    "nextStep" TEXT,
    "distToNextStep" REAL,
    "desiredHeading" REAL,
    "currentX" REAL NOT NULL DEFAULT 0,
    "currentY" REAL NOT NULL DEFAULT 0,
    "heading" REAL NOT NULL DEFAULT 0
);
INSERT INTO "new_NavigationState" ("currentX", "currentY", "desiredHeading", "distToNextStep", "heading", "id", "nextStep", "route", "state") SELECT "currentX", "currentY", "desiredHeading", "distToNextStep", "heading", "id", "nextStep", "route", "state" FROM "NavigationState";
DROP TABLE "NavigationState";
ALTER TABLE "new_NavigationState" RENAME TO "NavigationState";
PRAGMA foreign_key_check;
PRAGMA foreign_keys=ON;
