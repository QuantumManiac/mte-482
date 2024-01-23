import { db } from "~/server/db";

export default async function Home() {
  const products = await db.product.findMany()
  return (
    <main>
        <h1>Products</h1>
        <ul>
          {(products).map((product) => <li key={product.id}>{product.name}</li>)}
        </ul>
    </main>
  );
}
