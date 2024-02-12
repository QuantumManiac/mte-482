import { type Product} from "@prisma/client";
import ProductsList from "./ProductsList";
import ShoppingCartList from "./ShoppingCartList";

interface ItemListContainerProps {
    allItems: Product[];
    handleAddToCart: (item: Product) => void;
    handleRemoveFromCart: (id: number) => void;
}

export default function ItemListContainer({ allItems, handleRemoveFromCart, handleAddToCart }: ItemListContainerProps) {
    const shoppingCartItems = allItems.filter((item) => item.inCart);

    return (
    <div className="flex flex-1 h-screen">
      <ShoppingCartList shoppingCart={shoppingCartItems} handleRemoveFromCart={handleRemoveFromCart} />
      <ProductsList products={allItems} handleAddToCart={handleAddToCart}/>
    </div>
    );
    }
