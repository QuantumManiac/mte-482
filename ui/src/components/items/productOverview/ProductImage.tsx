import { type Product } from "@prisma/client";
import Image from 'next/image'

interface ProductImageProps {
    product: Product
}

export default function ProductImage({ product }: ProductImageProps) {
    return (
        <div className="h-full w-full relative">
            <Image src={`/img/products/${product.image ?? "no-image.jpg"}`} alt={product.name} layout="fill" objectFit="contain" />
        </div>
    );
}
