-- CreateTable
CREATE TABLE "NavigationState" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT DEFAULT 0,
    "state" TEXT NOT NULL DEFAULT 'idle',
    "routeTo" TEXT,
    "route" TEXT,
    "nextStep" TEXT,
    "distToNextStep" REAL,
    "currentX" REAL NOT NULL DEFAULT 0,
    "currentY" REAL NOT NULL DEFAULT 0,
    "heading" REAL NOT NULL DEFAULT 0
);
