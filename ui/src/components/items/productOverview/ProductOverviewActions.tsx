'use client'

import {type Product} from '@prisma/client'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

import ActionButton from '~/components/common/ActionButton'



interface ProductOverviewActionsProps {
    item?: Product;
    handleCartModify: (item: Product) => void;
}

export default function ProductOverviewActions(
    { item, handleCartModify }: ProductOverviewActionsProps
) {
    const router = useRouter()

    const [inCart, setInCart] = useState<boolean>(item?.inCart ?? false)

    const handleCartModifyAndState = async (item: Product) => {
        handleCartModify(item)
        setInCart(!inCart)
    }

    if (!item) {
        return (
            <div className="flex flex-row">
                <ActionButton icon="🔙" text="Back" onClick={() => router.back()}/>
            </div>
        )
    } else {
        return (
            <div className="flex flex-row">
                <ActionButton style="bg-yellow-300 flex-1" icon="🔙" text="Back" onClick={() => router.back()}/>
                {inCart ? <ActionButton style="bg-red-300 flex-1" icon="❌" text="Remove from Cart" onClick={() => handleCartModifyAndState(item)}/> : <ActionButton style="bg-green-300 flex-1" icon="➕" text="Add to Cart" onClick={() => handleCartModifyAndState(item)}/>}
                <ActionButton style="bg-blue-300 flex-1" icon="🗺️" text="Navigate To"/>
            </div>
        )
    }

}
