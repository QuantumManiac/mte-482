'use client';

import BatteryIndicator from "./BatteryIndicator";
import PushAssistIndicator from "./PushAssistIndicator";
import { useEffect, useState } from "react";
import { io, type Socket } from "socket.io-client";
import { env } from "~/env"
import PowerStateListener from "./PowerStateListener";

interface ServerToClientEvents {
    battery_voltage: (b: number) => void;
    push_assist_enabled: (e: boolean) => void;
    push_assist_throttle: (t: number) => void;
}

interface ClientToServerEvents {
    ui_message: ({topic, msg}: {topic: string, msg: string}) => void;
}

export default function StatusBar() {
    useEffect(() => {
        function onBatteryEvent(battery: number) {
            setBattery(battery);
        }

        function onPushAssistEnabledEvent(enabled: boolean) {
            setPushAssistEnabled(enabled);
        }

        function onPushAssistThrottleEvent(throttle: number) {
            setPushAssistThrottle(throttle);
        }

        const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(env.NEXT_PUBLIC_SOCKETIO_PORT)
        socket.on('push_assist_enabled', onPushAssistEnabledEvent);
        socket.on('push_assist_throttle', onPushAssistThrottleEvent);
        socket.on('battery_voltage', onBatteryEvent);

        return () => {
            socket.disconnect();
            socket.off('battery_voltage', onBatteryEvent);
            socket.off('push_assist_enabled', onPushAssistEnabledEvent);
            socket.off('push_assist_throttle', onPushAssistThrottleEvent);
        }
    }
    , []);

    const [battery, setBattery] = useState<number | undefined>(undefined);
    const [pushAssistEnabled, setPushAssistEnabled] = useState<boolean>(false);
    const [pushAssistThrottle, setPushAssistThrottle] = useState<number | undefined>(undefined);

    return (
        <div className=" text-white text-sm p-3">
            <BatteryIndicator value={battery}/>
            <PushAssistIndicator active={pushAssistEnabled} throttle={pushAssistThrottle}/>
            <PowerStateListener />
        </div>
    )
}
