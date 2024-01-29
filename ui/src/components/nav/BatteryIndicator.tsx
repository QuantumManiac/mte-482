'use client';

import { useEffect, useState } from "react"
import * as zmq from "jszmq"
import { env } from "~/env";

export default function BatteryIndicator() {
    const [batteryLevel, setBatteryLevel] = useState<number | null>(null);

    useEffect(() => {
        const socket = new zmq.Sub()
        socket.connect(env.NEXT_PUBLIC_ZEROMQ_SUB_URL);
        
        socket.subscribe("battery");
        socket.on("message", (topic, message: string) => {
            console.log("BatteryIndicator received message:", message);
        })
        
        return () => {
            socket.close();
        }
    }, []);


    return (
        <div className="border text-white border-white text-sm p-3">
            <h1>Battery Percent: {batteryLevel ? batteryLevel : "???"}</h1>
        </div>
    )
}
