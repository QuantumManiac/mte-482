"use client"

import { type Product } from "@prisma/client";
import ProductListItem from "./ProductListItem";
import { useState} from "react";
import ProductsListSearchBar from "./ProductsListSearchBar";


interface ProductsListProps {
    products: Product[];
    handleAddToCart: (item: Product) => void;
    addedToCart: Set<number>;
}

export default function ProductsList({ products, handleAddToCart, addedToCart }: ProductsListProps) {
    const [search, setSearch] = useState("");
    const [filteredProducts, setFilteredProducts] = useState<Product[]>(products);


    const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearch(e.target.value);
        const filteredProducts = products.filter((product) => product.name.toLowerCase().includes(e.target.value.toLowerCase()))
        setFilteredProducts(filteredProducts)
    };

    const handleAddToCartAndSetState = (item: Product) => {
        handleAddToCart(item);
    }

    return (
        <div className="flex-1 border-r-2 border-black flex flex-col">
            <ProductsListSearchBar handleSearch={handleSearch} search={search} />
            <div className="overflow-y-scroll flex-1">
                {filteredProducts.map((product: Product) => (
                    <ProductListItem key={product.id} handleAddToCart={handleAddToCartAndSetState} product={product} addedToCart={addedToCart.has(product.id)}/>
                ))}
            </div>
        </div>
    );
}
