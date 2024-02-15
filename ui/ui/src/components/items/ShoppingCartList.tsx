'use client';
import { type Product} from "@prisma/client";
import ShoppingCartListItem from "./ShoppingCartListItem";
import { useState, useEffect } from "react";

interface  ShoppingCartListProps {
    products: Product[]
    handleRemoveFromCart: (id: number) => void;
    addedToCart: Set<number>;
}

export default function ShoppingCartList({ products, handleRemoveFromCart, addedToCart}: ShoppingCartListProps) {
    const [shoppingCart, setShoppingCart] = useState<Product[]>(products.filter((product) => product.inCart));
    
    useEffect(() => {   
        setShoppingCart(products.filter((product) => addedToCart.has(product.id)));
    }
    , [products, addedToCart]);


    return (
        <div className="border-r-2 border-black flex-1 flex flex-col">
            <div className="text-2xl border-b-2 p-px border-black text-center">
                <h1>Shopping Cart</h1>
            </div>
            <div className="overflow-y-scroll flex-1">
                {shoppingCart.map((cartItem) => (
                    <ShoppingCartListItem key={cartItem.id} cartItem={cartItem} handleRemoveFromCart={handleRemoveFromCart} />
                ))}
            </div>
        </div>
    );
}
