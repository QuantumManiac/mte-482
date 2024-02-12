'use client';
import { useState } from "react";
import { type Product} from "@prisma/client";
import ShoppingCartListItem from "./ShoppingCartListItem";

interface  ShoppingCartListProps {
    shoppingCart: Product[]
    handleRemoveFromCart: (id: number) => void;
}

export default function ShoppingCartList({ shoppingCart, handleRemoveFromCart }: ShoppingCartListProps) {
    const [cartItems, setCartItems] = useState<Product[]>(shoppingCart);

    const handleRemoveFromCartAndSetState = (id: number) => {
        handleRemoveFromCart(id);
        setCartItems((prevCartItems) => prevCartItems.filter((cartItem) => cartItem.id !== id));
    }

    return (
        <div className="border border-black flex-1">
            <h1>Shopping Cart</h1>
            {cartItems.map((cartItem) => (
                <ShoppingCartListItem key={cartItem.id} cartItem={cartItem} handleRemoveFromCart={handleRemoveFromCartAndSetState} />
            ))}
        </div>
    );

}
