import { type Product } from "@prisma/client";
import ItemListContainer from "~/components/items/ItemListContainer";
import { db } from "~/server/db";

import { revalidatePath } from 'next/cache';

import { unstable_noStore as noStore } from 'next/cache';

export default async function Page() {
  noStore();
  async function handleAddToCart(item: Product): Promise<void> {
    'use server'
    const id = item.id;
    await db.product.update({
      where: { id },
      data: {
        inCart: true,
        done: false
      },
    });
    revalidatePath('/');
  };

  async function handleRemoveFromCart(id: number): Promise<void> {
    'use server'
    await db.product.update({
      where: { id },
      data: {
        inCart: false,
        done: false,
      },
    });
    revalidatePath('/(main)');
  };

  async function handleToggleDone(product: Product): Promise<void> {
    'use server'
    await db.product.update({
      where: { id: product.id },
      data: {
        done: !product.done,
      },
    });
    revalidatePath('/(main)');
  }
  
  const allItems = await db.product.findMany();

  return (
    <ItemListContainer initialItems={allItems} handleAddToCart={handleAddToCart} handleRemoveFromCart={handleRemoveFromCart} handleToggleDone={handleToggleDone} />
  );
}
