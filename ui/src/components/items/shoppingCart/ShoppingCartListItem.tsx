'use client'

import { useState } from "react";
import { type Product } from "@prisma/client";
import ProductImage from '../ProductImage';
import ActionButton from "~/components/common/ActionButton";

import clsx from "clsx";


interface ShoppingCartListItemProps {
    cartItem: Product;
    handleRemoveFromCart: (id: number) => void;
    handleToggleDone: (product: Product) => void;
}

export default function ShoppingCartListItem({ cartItem, handleRemoveFromCart, handleToggleDone }: ShoppingCartListItemProps) {
    const [checked, setChecked] = useState(cartItem.done);
    
    const handleCheckbox = () => {
        setChecked(!checked);
        handleToggleDone(cartItem);
    }

    return (
        <div className={clsx(
            "border-b-4 border-slate-500 flex flex-row",
            checked ? "bg-green-200" : "bg-slate-200"
        )}>
            
            <input className="scale-[2] mx-5" type="checkbox" checked={checked} onChange={handleCheckbox} />
            <h3 className={clsx(
                "grow text-xl pl-2 text-balance",
                checked && "line-through"
            )}>{cartItem.name}</h3>
            <div className="flex flex-row">
            <ActionButton style="bg-orange-300" icon="🗺️" text="Navigate" onClick={() => {console.log("Navigating to " + cartItem.location)}}/>
            <ActionButton style="bg-blue-300" icon="🔍" text="View" onClick={() => {window.location.href = `/items/${cartItem.id}`}}/>
            <ActionButton style="bg-red-300" icon="❌" text="Remove" onClick={() => handleRemoveFromCart(cartItem.id)}/>
            </div>
        </div>
    );
}
