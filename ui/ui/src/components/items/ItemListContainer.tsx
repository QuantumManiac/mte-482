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

export default function ItemListContainer({ allItems, handleAddToCart, handleRemoveFromCart }: ItemListContainerProps) {
    const shoppingCartItems = allItems.filter((item) => item.inCart)

    const handleAddToCartAndState = (item: Product) => {
        handleAddToCart(item);
        setShoppingCartItems([...shoppingCartItems, item]);
    }

    const handleRemoveFromCartAndState = (id: number) => {
        handleRemoveFromCart(id);
        setShoppingCartItems(shoppingCartItems.filter((cartItem) => cartItem.id !== id));
    }

    return (
    <div className="flex flex-1 h-screen">
      <ShoppingCartList shoppingCart={shoppingCartItems} handleRemoveFromCart={handleRemoveFromCartAndState} />
      <ProductsList products={allItems} handleAddToCart={handleAddToCartAndState}/>
    </div>
    );
    }
