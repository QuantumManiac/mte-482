/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { type Product } from '@prisma/client'

import ExpandedViewText from '~/components/common/ExpandedViewText';

interface ProductAdditionalInfoProps {
    product: Product
    }

export default function ProductAdditionalInfo({product}: ProductAdditionalInfoProps) {
  return (
    <div className='p-2 h-full text-lg relative'>
        {product.additionalInfo ? <p>{product.additionalInfo}</p> : <p className='italic'>(No additional info)</p>}
        {product.additionalInfo ? <ExpandedViewText text={product.additionalInfo}/> : null}
    </div>
  );
}
