import { type Product } from '@prisma/client'

interface ProductDetailsProps {
    product: Product
    }

export default function ProductDetails({product}: ProductDetailsProps) {
  return (
  <div className="relative flex flex-col h-full">
      <h1 className="text-3xl font-bold">{product.name}</h1>
      <p className="text-2xl font-bold">${product.price.toFixed(2)}</p>
      <p className="text-2xl font-bold">{product.location}</p>
      <p className="italic mt-auto text-slate-500">ID: {product.id} RFID: {product.rfid ?? "N/A"}</p>
  </div>
  );
}
