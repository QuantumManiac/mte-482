'use client'

import { type Product} from "@prisma/client";
import ProductsList from "./productList/ProductsList";
import ShoppingCartList from "./shoppingCart/ShoppingCartList";

import { useState } from "react";

interface ItemListContainerProps {
    allItems: Product[];
    handleAddToCart: (item: Product) => void;
    handleRemoveFromCart: (id: number) => void;
    handleToggleDone: (product: Product) => void;
}

export default function ItemListContainer({ allItems, handleRemoveFromCart, handleAddToCart, handleToggleDone }: ItemListContainerProps) {
    const [addedToCart, setAddedToCart] = useState(() => {
        const addedToCart = new Set<number>();
        allItems.forEach((product) => {
            if (product.inCart) {
                addedToCart.add(product.id);
            }
        });

        return addedToCart;
    });

    const handleAddToCartAndSetState = (item: Product) => {
        handleAddToCart(item);
        setAddedToCart((prevAddedToCart) => {
            const newAddedToCart = new Set(prevAddedToCart);
            newAddedToCart.add(item.id);
            return newAddedToCart;
        }
        )
    }

    const handleRemoveFromCartAndSetState = (id: number) => {
        handleRemoveFromCart(id);
        setAddedToCart((prevAddedToCart) => {
            const newAddedToCart = new Set(prevAddedToCart);
            newAddedToCart.delete(id);
            return newAddedToCart;
        }
        );
    }

    return (
    <div className="flex flex-1 h-screen space-x-1 bg-slate-300">
      <ShoppingCartList products={allItems} addedToCart={addedToCart} handleRemoveFromCart={handleRemoveFromCartAndSetState} handleToggleDone={handleToggleDone} />
      <ProductsList products={allItems} addedToCart={addedToCart} handleAddToCart={handleAddToCartAndSetState}/>
    </div>
    );
    }
