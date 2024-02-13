'use client'

import { useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";
import { env } from "~/env";


export default function ScanListener() {
    const [rfid, setRfid] = useState<string | undefined>("");

    interface ServerToClientEvents {
        zmq_rfid: (b: string) => void;
    }

    useEffect(() => {
        function onRfidEvent(rfid: string) {
            if (rfid != "00-00-00-00") {
                setRfid(rfid);
            }
        }

        const socket: Socket<ServerToClientEvents> = io(env.NEXT_PUBLIC_SOCKETIO_PORT)
        socket.on('zmq_rfid', onRfidEvent);

        return () => {
            socket.disconnect();
            socket.off('zmq_rfid', onRfidEvent);
        }
    }
    , []);

    return (
        <main>
            {rfid ? rfid : "Scanning..."}
        </main>
    )
}