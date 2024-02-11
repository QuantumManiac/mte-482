'use client';

import clsx from "clsx";

interface BatteryIndicatorProps {
    value?: number;
}

enum BatteryStatus {
    CRITICAL = "CRITICAL",
    LOW = "LOW",
    NORMAL = "NORMAL",
    UNKNOWN = "UNKNOWN"
}

function getBatteryStatus(value: number | undefined): BatteryStatus {
    if (value === undefined) {
        return BatteryStatus.UNKNOWN;
    }
    
    if (value > 13.5) {
        return BatteryStatus.NORMAL;
    }

    if (value >= 12.8 && value < 13.5) {
        return BatteryStatus.LOW;
    }

    return BatteryStatus.CRITICAL;
}

export default function BatteryIndicator({value}: BatteryIndicatorProps) {
    const batteryStatus = getBatteryStatus(value);

    return (
        <div className={
            clsx(
                "text-white border-white text-sm",
                {
                    "font-bold text-red-500": batteryStatus === BatteryStatus.CRITICAL || batteryStatus === BatteryStatus.UNKNOWN,
                    "text-yellow-500": batteryStatus === BatteryStatus.LOW,
                    "text-green-500": batteryStatus
                }
            )
        }>
            <h1>Battery: {value ? value : "???"} V</h1>
        </div>
    )
}
