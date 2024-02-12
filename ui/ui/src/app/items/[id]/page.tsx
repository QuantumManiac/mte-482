import { db } from '~/server/db'

export default async function Page({params} : {params: {id: string}}) {

    const item  = await db.product.findFirst({
        where: { id: Number(params.id) },
    })

    if (!item) {
        return <div>Item not found</div>
    }

    return (
        <main>
            <h1>{item.name}</h1>
            <p>{item.description}</p>
            <p>{item.price}</p>
        </main>
    )
}
