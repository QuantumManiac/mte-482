'use client' 

import clsx from "clsx";
import { usePathname } from "next/navigation";

interface NavLinkProps {
    name: string;
    path: string;
}

export default function NavLink({name, path}: NavLinkProps) {
    const pathName = usePathname();
    return (
      <a href={path} className={
            clsx(
              "border-y border-white flex grow items-center justify-center text-xl",
              {
                "bg-gray-800": pathName === path,
                "bg-gray-600": pathName !== path,
              }
            )
        }
        >
          
            <h1 className="text-center text-white font-bold text-lg p-5">{name}</h1>
    </a>
    )

}
