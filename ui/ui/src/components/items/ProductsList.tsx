

import { type Product } from "@prisma/client";
import ProductListItem from "./ProductListItem";
import { useState } from "react";
import ProductsListSearchBar from "./ProductsListSearchBar";


interface ProductsListProps {
    products: Product[];
    handleAddToCart: (item: Product) => void;
}

export default function ProductsList({ products, handleAddToCart }: ProductsListProps) {
    const [search, setSearch] = useState("");
    const [filteredProducts, setFilteredProducts] = useState(products);

    const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearch(e.target.value);
        setFilteredProducts(
            products.filter((product) => product.name.toLowerCase().includes(e.target.value.toLowerCase())
            )
        );
    };

    return (
        <div className="border border-black flex-1">
            <ProductsListSearchBar handleSearch={handleSearch} search={search} />
            {filteredProducts.map((product: Product) => (
                <ProductListItem key={product.id} product={product} handleAddToCart={handleAddToCart} />
            ))}
        </div>
    );
}
