import { type Product } from '@prisma/client'

import ExpandedViewText from '~/components/common/ExpandedViewText';

interface ProductDescriptionProps {
    product: Product
    }

export default function ProductDescription({product}: ProductDescriptionProps) {
  return (
    <div className='p-2 h-full relative'>
        <p>{product.description}</p>
        <ExpandedViewText text={product.description}/>
    </div>
  );
}
