"use client"

import { type Product } from "@prisma/client";
import ProductListItem from "./ProductListItem";
import { useState} from "react";
import ProductsListSearchBar from "./ProductsListSearchBar";


interface ProductsListProps {
    products: Product[];
    handleAddToCart: (item: Product) => void;
}

export default function ProductsList({ products, handleAddToCart }: ProductsListProps) {
    const [search, setSearch] = useState("");
    const [filteredProducts, setFilteredProducts] = useState<Product[]>(products);

    const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearch(e.target.value);
        setFilteredProducts(
            products.filter((product) => product.name.toLowerCase().includes(e.target.value.toLowerCase())
            )
        );
    };

    return (
        <div className="flex-1 border-r-2 border-black">
            <ProductsListSearchBar handleSearch={handleSearch} search={search} />
            <div className="overflow-y-scroll">
                {filteredProducts.map((product: Product) => (
                    <ProductListItem key={product.id} handleAddToCart={handleAddToCart} product={product}/>
                ))}
            </div>
        </div>
    );
}
