'use client';

import BatteryIndicator from "./BatteryIndicator";
import { useEffect, useState } from "react";
import { io, type Socket } from "socket.io-client";
import { env } from "~/env"

interface ServerToClientEvents {
    zmq_battery_voltage: (b: number) => void;
}

interface ClientToServerEvents {
    ui_message: ({topic, msg}: {topic: string, msg: string}) => void;
}

export default function StatusBar() {
    useEffect(() => {
        function onBatteryEvent(battery: number) {
            setBattery(battery);
        }

        const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(env.NEXT_PUBLIC_SOCKETIO_PORT)
        console.log("Connected to socket.io server");
        socket.on('zmq_battery_voltage', onBatteryEvent);

        return () => {
            socket.disconnect();
            socket.off('zmq_battery_voltage', onBatteryEvent);
        }
    }
    , []);

    const [battery, setBattery] = useState<number | undefined>(0);

    return (
        <div className="border-b text-white border-white text-sm p-3">
            <BatteryIndicator value={battery}/>
        </div>
    )
}
