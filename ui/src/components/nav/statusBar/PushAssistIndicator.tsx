'use client'

import clsx from "clsx";

interface PushAssistIndicatorProps {
    active: boolean;
    throttle?: number;
}

export default function PushAssistIndicator({active, throttle}: PushAssistIndicatorProps) {
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
        >Push Assist: {active ? `ON (${throttle ?? "???"})` : "OFF"}</h1>
    )

}
