'use client'

import { type Product } from "@prisma/client";

interface ProductListItemProps {
    product: Product;
    handleAddToCart: (item: Product) => void;
}

export default function ProductListItem({ product, handleAddToCart }: ProductListItemProps) {
    return (
        <div className="border">
            <h3>{product.name}</h3>
            <a href={`/items/${product.id}`}>View</a>
            <button onClick={() => handleAddToCart(product)}>Add</button>
        </div>
    );
}
