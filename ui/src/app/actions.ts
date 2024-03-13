"use server";

import { Product } from "@prisma/client";
import { db } from "~/server/db";

import { NavState } from "~/types/Navigation";

export async function getIdFromRfid(rfid: string): Promise<number | undefined> {
  "use server";
  if (rfid == "00-00-00-00") return;
  const item = await db.product.findFirst({
    where: {
      rfid: rfid,
    },
  });
  return item?.id;
}

export async function cancelRoute(): Promise<void> {
  "use server";
  await db.navigationState.update({
    where: { id: 0 },
    data: {
      state: NavState.PENDING_CANCEL,
    },
  });
}

interface Destination {
  name: string;
  x: number | null;
  y: number | null;
}

export async function startRoute(dest: Destination): Promise<void> {
  "use server";
  await db.navigationState.update({
    where: { id: 0 },
    data: {
      state: NavState.START_NAV,
      destName: dest.name,
      destX: dest.x,
      destY: dest.y,
    },
  });
}
