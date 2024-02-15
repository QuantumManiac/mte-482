'use server'

import { db } from "~/server/db";

export async function getIdFromRfid(rfid: string): Promise<number | undefined> {
    'use server'
    const item = await db.product.findFirst({
      where: {
        rfid: rfid
      }
    });
    return item?.id;
}
