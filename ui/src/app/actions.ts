"use server";

import { db } from "~/server/db";

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
