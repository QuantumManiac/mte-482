
import { type Product} from "@prisma/client";
import ShoppingCartListItem from "./ShoppingCartListItem";
import { useState } from "react";


interface  ShoppingCartListProps {
    shoppingCart: Product[]
    handleRemoveFromCart: (id: number) => void;
}

export default function ShoppingCartList({ shoppingCart, handleRemoveFromCart }: ShoppingCartListProps) {
    return (
        <div className="border border-black flex-1">
            <h1>Shopping Cart</h1>
            {shoppingCart.map((cartItem) => (
                <ShoppingCartListItem key={cartItem.id} cartItem={cartItem} handleRemoveFromCart={handleRemoveFromCart} />
            ))}
        </div>
    );

}
