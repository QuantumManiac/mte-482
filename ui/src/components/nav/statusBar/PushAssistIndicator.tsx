'use client'

import clsx from "clsx";

interface PushAssistIndicatorProps {
    active: boolean[];
}

export default function PushAssistIndicator({active}: PushAssistIndicatorProps) {
    // eslint-disable-next-line @typescript-eslint/prefer-nullish-coalescing
    const isActive = active[0] || active[1];
    return (
        <h1 className={
            clsx(
                " border-white text-sm",
                {
                    "font-bold text-green-500": isActive,
                    "text-white-500": !isActive
                }
            )
        }
        >Push Assist: {active[1] ? "ON" : "OFF"}/{active[0] ? "ON" : "OFF"}</h1>
    )

}
