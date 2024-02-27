import { type Product } from "@prisma/client";
import ItemListContainer from "~/components/items/ItemListContainer";
import { db } from "~/server/db";

export default async function Page() {
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
  };

  async function handleToggleDone(product: Product): Promise<void> {
    'use server'
    await db.product.update({
      where: { id: product.id },
      data: {
        done: !product.done,
      },
    });
  }
  
  const allItems = await db.product.findMany();

  return (
    <ItemListContainer allItems={allItems} handleAddToCart={handleAddToCart} handleRemoveFromCart={handleRemoveFromCart} handleToggleDone={handleToggleDone} />
  );
}
