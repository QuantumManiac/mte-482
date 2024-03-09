'use client'

import { type Product } from "@prisma/client";

import ProductImage from "../productOverview/ProductImage";
import ActionButton from "~/components/common/ActionButton";

interface ProductListItemProps {
    product: Product;
    handleAddToCart: (item: Product) => void;
    addedToCart: boolean;
}

export default function ProductListItem({ product, handleAddToCart, addedToCart }: ProductListItemProps) {
    return (
        <div className="border-b-4 border-slate-500 flex flex-row bg-slate-200">
            <h3 className="grow text-xl pl-2">{product.name}</h3>
            <div className="flex flex-row">
                <ActionButton style="bg-orange-300" icon="🗺️" text="Navigate" onClick={() => {console.log("Navigating to " + product.location)}}/>
                <ActionButton style="bg-blue-300" icon="🔍" text="View" onClick={() => {window.location.href = `/items/${product.id}`}}/>
                {addedToCart ? <ActionButton disabled style="bg-slate-300" icon="☑️" text="(Added)"/> : <ActionButton style="bg-green-300" icon="➕" text="Add" onClick={() => handleAddToCart(product)}/>}
            </div>
        </div>
    );
}
