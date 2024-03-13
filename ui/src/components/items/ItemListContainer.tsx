'use client'

import { type Product} from "@prisma/client";
import ProductsList from "./productList/ProductsList";
import ShoppingCartList from "./shoppingCart/ShoppingCartList";

import { useState } from "react";

interface ItemListContainerProps {
    initialItems: Product[];
    handleAddToCart: (item: Product) => void;
    handleRemoveFromCart: (id: number) => void;
    handleToggleDone: (product: Product) => void;
}

export default function ItemListContainer({ initialItems, handleRemoveFromCart, handleAddToCart, handleToggleDone }: ItemListContainerProps) {
    const [allItems, setAllItems] = useState<Map<number, Product>>(new Map(initialItems.map(obj => [obj.id, obj])));

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
        });

        setAllItems((prevAllItems) => {
            const newAllItems = new Map(prevAllItems);
            newAllItems.set(item.id, { ...item, inCart: true, done: false});
            return newAllItems;
        })
    }

    const handleRemoveFromCartAndSetState = (id: number) => {
        handleRemoveFromCart(id);
        setAddedToCart((prevAddedToCart) => {
            const newAddedToCart = new Set(prevAddedToCart);
            newAddedToCart.delete(id);
            return newAddedToCart;
        });

        setAllItems((prevAllItems) => {
            const item = prevAllItems.get(id);
            if (!item) {
                return prevAllItems;
            }
            const newAllItems = new Map(prevAllItems);
            newAllItems.set(id, { ...item, inCart: false });
            return newAllItems;
        })
    }

    return (
    <div className="flex flex-1 h-screen space-x-1 bg-slate-300">
      <ShoppingCartList products={Array.from(allItems.values())} addedToCart={addedToCart} handleRemoveFromCart={handleRemoveFromCartAndSetState} handleToggleDone={handleToggleDone} />
      <ProductsList products={Array.from(allItems.values())} addedToCart={addedToCart} handleAddToCart={handleAddToCartAndSetState}/>
    </div>
    );
    }
