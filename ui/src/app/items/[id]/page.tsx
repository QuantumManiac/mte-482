import { db } from '~/server/db'

import type { Product } from '@prisma/client'

import ProductOverviewActions from '~/components/items/productOverview/ProductOverviewActions';

export default async function Page({params} : {params: {id: string}}) {
    const item  = await db.product.findFirst({
        where: { id: Number(params.id) },
    })

    async function handleCartModify(item: Product): Promise<void> {
        'use server'
        const id = item.id;
        await db.product.update({
            where: { id },
            data: {
                inCart: !item.inCart,
            },
        });
    }

    if (!item) {
        return <div>Item not found</div>
    }

    return (
        <main>
            <div className="flex flex-1 h-screen space-x-1 bg-slate-300">
                <ProductOverviewActions item={item} handleCartModify={handleCartModify} />
                <div className="flex flex-col">
                    <h1 className="text-4xl">{item.name}</h1>
                    <p>{item.description}</p>
                    <p>{item.price}</p>
                </div>
            </div>
        </main>
    )
}
