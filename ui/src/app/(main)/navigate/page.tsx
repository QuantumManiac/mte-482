import NavigationContainer from "~/components/navigation/NavigationContainer";
import { type NavigationState } from "@prisma/client";
import { db } from "~/server/db";

export default async function Page() {
  const navigationState = await db.navigationState.findFirst();
  const cartItems = await db.product.findMany({
    where: {
      inCart: true
    },
  
  })
  async function getNavigationState(): Promise<NavigationState | null> {
    'use server';
    return await db.navigationState.findFirst();
  }

  return (
    <main>
      <NavigationContainer initialNavigationState={navigationState} getNavigationState={getNavigationState} cartItems={cartItems} />
    </main>
  );
}
