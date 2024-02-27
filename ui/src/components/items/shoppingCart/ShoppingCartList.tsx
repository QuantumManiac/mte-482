'use client';
import { type Product} from "@prisma/client";
import ShoppingCartListItem from "./ShoppingCartListItem";
import { useState, useEffect } from "react";

interface  ShoppingCartListProps {
    products: Product[]
    handleRemoveFromCart: (id: number) => void;
    handleToggleDone: (product: Product) => void;
    addedToCart: Set<number>;
}

export default function ShoppingCartList({ products, handleRemoveFromCart, addedToCart, handleToggleDone}: ShoppingCartListProps) {
    const [shoppingCart, setShoppingCart] = useState<Product[]>(products.filter((product) => product.inCart));
    
    useEffect(() => {   
        setShoppingCart(products.filter((product) => addedToCart.has(product.id)));
    }
    , [products, addedToCart]);


    return (
        <div className="flex-1 flex flex-col bg-slate-100">
            <div className="text-2xl border-b-2 bg-slate-300 border-black text-center">
                <h1>Shopping Cart</h1>
            </div>
            <div className="overflow-y-scroll flex-1">
                {shoppingCart.map((cartItem) => (
                    <ShoppingCartListItem key={cartItem.id} cartItem={cartItem} handleRemoveFromCart={handleRemoveFromCart} handleToggleDone={handleToggleDone}/>
                ))}
            </div>
        </div>
    );
}
