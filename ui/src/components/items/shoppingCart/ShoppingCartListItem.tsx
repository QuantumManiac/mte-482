'use client'

import { useState } from "react";
import { type Product } from "@prisma/client";
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
            <input className="scale-[2] mx-5 my-5" type="checkbox" checked={checked} onChange={handleCheckbox} />
            <div className={clsx(
                    "grow pl-2",
                    checked && "line-through"
                )}>
                <h3 className={"text-xl text-balance"}>{cartItem.name}</h3>
                <p className="text">{cartItem.locationText}</p>
            </div>
            <div className="flex flex-row">
                <ActionButton style="bg-orange-300" icon="🗺️" text="Navigate" onClick={() => {console.log("Navigating to " + cartItem.locationText)}}/>
                <ActionButton style="bg-blue-300" icon="🔍" text="View" onClick={() => {window.location.href = `/items/${cartItem.id}`}}/>
                <ActionButton style="bg-red-300" icon="❌" text="Remove" onClick={() => handleRemoveFromCart(cartItem.id)}/>
            </div>
        </div>
    );
}
