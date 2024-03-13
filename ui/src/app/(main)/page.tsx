import DashboardShoppingCartList from "~/components/dashboard/DashboardShoppingCartList";
import DashboardNavigationContainer from "~/components/dashboard/DashboardNavigationContainer";

import type { Product, NavigationState } from "@prisma/client";

import { db } from "~/server/db";

import { unstable_noStore as noStore } from 'next/cache';

import { revalidatePath } from 'next/cache';

export default async function Home() {
    noStore();
    const shoppingCart = await db.product.findMany({
        where: {
            inCart: true,
        },
    });

    const navigationState = await db.navigationState.findFirst();

    async function handleRemoveFromCart(id: number): Promise<void> {
        'use server'
        await db.product.update({
            where: { id },
            data: {
                inCart: false,
                done: false,
            },
        });
        revalidatePath('/items');
    };

    async function handleToggleDone(product: Product): Promise<void> {
        'use server'
        await db.product.update({
            where: { id: product.id },
            data: {
                done: !product.done,
            },
        });
        revalidatePath('/items');
    }

    async function getNavigationState(): Promise<NavigationState | null> {
        'use server'
        return await db.navigationState.findFirst();
    }

    return (
      <div className="flex space-x-1 bg-slate-300">
        <div className="flex-1 h-screen">
                <DashboardShoppingCartList initialShoppingCart={shoppingCart} handleRemoveFromCart={handleRemoveFromCart} handleToggleDone={handleToggleDone} />
        </div>
        <div className="flex-1 h-screen">
                <DashboardNavigationContainer initialNavigationState={navigationState} getNavigationState={getNavigationState} />
        </div>
      </div>
    );
}
