import { db } from '~/server/db'

import type { Product } from '@prisma/client'

import ProductImage from '~/components/items/productOverview/ProductImage';
import ProductOverviewActions from '~/components/items/productOverview/ProductOverviewActions';

import ProductDescription from '~/components/items/productOverview/ProductDescription';
import ProductDetails from '~/components/items/productOverview/ProductDetails';
import ProductAdditionalInfo from '~/components/items/productOverview/ProductAdditionalInfo';

export default async function Page({params} : {params: {id: string}}) {
    const item  = await db.product.findFirst({
        where: { id: Number(params.id) },
    })

    async function handleCartModify(item: Product): Promise<void> {
        'use server'
        const id = item.id;

        const dbItem = await db.product.findFirst({
            where: { id },
        });

        if (!dbItem) {
            return;
        }

        await db.product.update({
            where: { id },
            data: {
                inCart: !dbItem.inCart,
                done: false,
            },
        });
    }

    if (!item) {
        return <div>Item not found</div>
    }

    return (
        <main>
            <div className="flex flex-col flex-1 space-y-1 h-screen bg-slate-300">
                <div className="flex grow space-x-1">
                    <div className='flex-1 flex flex-col space-y-1'>
                        <div className='bg-white flex-1 '>
                            <ProductImage product={item}/>
                        </div>
                        <div className='bg-white flex-1 px-2'>
                            <ProductDetails product={item}/>
                        </div>
                    </div>
                    <div className='bg-yellow-200 flex-1'>
                        <ProductDescription product={item}/>
                    </div>
                    <div className='bg-green-200 flex-1'>
                        <ProductAdditionalInfo product={item}/>
                    </div>
                </div>
                <ProductOverviewActions item={item} handleCartModify={handleCartModify} />
            </div>
        </main>
    )
}
