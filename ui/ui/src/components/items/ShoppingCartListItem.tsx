'use client'

import { type Product } from "@prisma/client";

interface ShoppingCartListItemProps {
    cartItem: Product;
    handleRemoveFromCart: (id: number) => void;
}

export default function ShoppingCartListItem({ cartItem, handleRemoveFromCart }: ShoppingCartListItemProps) {
    return (
        <div className="border">
            <h3>{cartItem.name}</h3>
            <p>{cartItem.location}</p>
            <button onClick={() => handleRemoveFromCart(cartItem.id)}>Remove</button>
        </div>
    );
}
