'use client';
import { type Product} from "@prisma/client";
import ShoppingCartListItem from "../items/shoppingCart/ShoppingCartListItem";
import { useState } from "react";

interface  ShoppingCartListProps {
    initialShoppingCart: Product[]
    handleRemoveFromCart: (id: number) => void;
    handleToggleDone: (product: Product) => void;
}

export default function DashboardShoppingCartList({ initialShoppingCart, handleRemoveFromCart, handleToggleDone}: ShoppingCartListProps) {
    const [shoppingCart, setShoppingCart] = useState<Product[]>(initialShoppingCart); 

    const handleRemoveFromCartAndState = (id: number) => {
        handleRemoveFromCart(id);
        setShoppingCart((prevShoppingCart) => {
            return prevShoppingCart.filter((product) => product.id !== id);
        });
    }

    const handleToggleDoneAndState = (product: Product) => {
        handleToggleDone(product);
        setShoppingCart((prevShoppingCart) => {
            return prevShoppingCart.map((cartItem) => {
                if (cartItem.id === product.id) {
                    return { ...cartItem, done: !cartItem.done };
                }
                return cartItem;
            });
        });
    }

    return (
        <div className="flex-1 flex flex-col bg-slate-100 h-screen">
            <div className="text-2xl border-b-2 bg-slate-200 border-black text-center">
                <h1>Shopping Cart</h1>
            </div>
            <div className="overflow-y-scroll flex-1">
                {shoppingCart.map((cartItem) => (
                    <ShoppingCartListItem key={cartItem.id} cartItem={cartItem} handleRemoveFromCart={handleRemoveFromCartAndState} handleToggleDone={handleToggleDoneAndState}/>
                ))}
            </div>
        </div>
    );
}
