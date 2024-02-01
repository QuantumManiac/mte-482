'use client';

interface BatteryIndicatorProps {
    value?: number;
}

export default function BatteryIndicator({value}: BatteryIndicatorProps) {



    return (
        <div className="border text-white border-white text-sm p-3">
            <h1>Battery Percent: {value ? value : "???"}</h1>
        </div>
    )
}
