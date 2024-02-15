'use client'

import { type Product} from "@prisma/client";
import ProductsList from "./ProductsList";
import ShoppingCartList from "./ShoppingCartList";

import { useState } from "react";

interface ItemListContainerProps {
    allItems: Product[];
    handleAddToCart: (item: Product) => void;
    handleRemoveFromCart: (id: number) => void;
}

export default function ItemListContainer({ allItems, handleRemoveFromCart, handleAddToCart }: ItemListContainerProps) {
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
    <div className="flex flex-1 h-screen">
      <ShoppingCartList products={allItems} addedToCart={addedToCart} handleRemoveFromCart={handleRemoveFromCartAndSetState} />
      <ProductsList products={allItems} addedToCart={addedToCart} handleAddToCart={handleAddToCartAndSetState}/>
    </div>
    );
    }
