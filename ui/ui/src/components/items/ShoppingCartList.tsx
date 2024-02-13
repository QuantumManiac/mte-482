'use client';
import { type Product} from "@prisma/client";
import ShoppingCartListItem from "./ShoppingCartListItem";

interface  ShoppingCartListProps {
    shoppingCart: Product[]
    handleRemoveFromCart: (id: number) => void;
}

export default function ShoppingCartList({ shoppingCart, handleRemoveFromCart }: ShoppingCartListProps) {
    return (
        <div className="border-r-2 border-black flex-1">
            <div className="text-2xl border-b-2 p-px border-black text-center">
                <h1>Shopping Cart</h1>
            </div>
            <div className="overflow-y-scroll">
                {shoppingCart.map((cartItem) => (
                    <ShoppingCartListItem key={cartItem.id} cartItem={cartItem} handleRemoveFromCart={handleRemoveFromCart} />
                ))}
            </div>
        </div>
    );
}
