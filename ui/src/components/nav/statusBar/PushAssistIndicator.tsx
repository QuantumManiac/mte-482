'use client'

import clsx from "clsx";

interface PushAssistIndicatorProps {
    active: boolean;
}

export default function PushAssistIndicator({active}: PushAssistIndicatorProps) {
    return (
        <h1 className={
            clsx(
                " border-white text-sm",
                {
                    "font-bold text-green-500": active,
                    "text-white-500": !active
                }
            )
        }
        >Push Assist: {active ? "ON" : "OFF"}</h1>
    )

}
