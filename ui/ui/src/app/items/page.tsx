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
      },
    });
  };

  async function handleRemoveFromCart(id: number): Promise<void> {
    'use server'
    await db.product.update({
      where: { id },
      data: {
        inCart: false,
      },
    });
  };
  
  const allItems = await db.product.findMany();

  return (
    <ItemListContainer allItems={allItems} handleAddToCart={handleAddToCart} handleRemoveFromCart={handleRemoveFromCart}/>
  );
}
