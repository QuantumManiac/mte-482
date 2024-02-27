import { type Product } from "@prisma/client";
import Image from 'next/image'
import { env } from "~/env";

interface ProductImageProps {
    product: Product
}

export default function ProductImage({ product }: ProductImageProps) {
    return (
        <div>
            <Image src={`/img/products/${product.image ?? "no-image.jpg"}`} alt={product.name} width={100} height={100} />
        </div>
    );
}
