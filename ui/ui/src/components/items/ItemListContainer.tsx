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
    const [shoppingCartItems, setShoppingCartItems] = useState<Product[]>(allItems.filter((item) => item.inCart));

    const handleAddToCartAndSetState = (item: Product) => {
        handleAddToCart(item);
        setShoppingCartItems((prevShoppingCartItems) => [...prevShoppingCartItems, item]);
    }

    const handleRemoveFromCartAndSetState = (id: number) => {
        handleRemoveFromCart(id);
        setShoppingCartItems((prevShoppingCartItems) => prevShoppingCartItems.filter((item) => item.id !== id));
    }

    return (
    <div className="flex flex-1 h-screen">
      <ShoppingCartList shoppingCart={shoppingCartItems} handleRemoveFromCart={handleRemoveFromCartAndSetState} />
      <ProductsList products={allItems} handleAddToCart={handleAddToCartAndSetState}/>
    </div>
    );
    }
