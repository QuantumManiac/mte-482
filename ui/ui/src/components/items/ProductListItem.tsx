'use client'

import { type Product } from "@prisma/client";

import { useState } from "react";

interface ProductListItemProps {
    product: Product;
    handleAddToCart: (item: Product) => void;
    addedToCart: boolean;
}

export default function ProductListItem({ product, handleAddToCart, addedToCart }: ProductListItemProps) {
    return (
        <div className="border">
            <h3>{product.name}</h3>
            <p>{product.description}</p>
            <a href={`/items/${product.id}`}>View</a>
            <br />
            {addedToCart ? <button disabled className="text-grey-500">(Added)</button> : <button className="text-green-500" onClick={() => handleAddToCart(product)}>Add</button>}
        </div>
    );
}
