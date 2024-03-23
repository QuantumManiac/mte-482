'use client';

import { useEffect } from "react";
import { io, type Socket } from "socket.io-client";
import { env } from "~/env"
import { useRouter } from "next/navigation";

interface ServerToClientEvents {
    power: (s: string) => void;
}

interface ClientToServerEvents {
    ui_message: ({topic, msg}: {topic: string, msg: string}) => void;
}

export default function PowerStateListener() {
    const router = useRouter();
    
    useEffect(() => {
        function onPowerStateEvent(s: string) {
            if (s === 'low') {
                router.push('/low-power');      
            }
        }

        const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(env.NEXT_PUBLIC_SOCKETIO_PORT)
        socket.on('power', onPowerStateEvent);

        return () => {
            socket.disconnect();
            socket.off('power', onPowerStateEvent);
        }
    }
    , []);

    return (
        <div className="hidden"/>
    )
}