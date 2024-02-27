'use client'

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { io, type Socket } from "socket.io-client";
import { env } from "~/env";
import { getIdFromRfid } from "~/app/actions";

export default function ScanListener() {
    interface ServerToClientEvents {
        zmq_rfid: (b: string) => void;
    }
    // TODO Make background green when valid RFID is scanned

    const [invalidRfid, setInvalidRfid] = useState<string | undefined>(undefined);

    const router = useRouter();
    useEffect(() => {
        
        
        async function onRfidEvent(rfid: string) {
            const id = await getIdFromRfid(rfid);
            console.log('id', id);
            if (id) {
                router.push(`/items/${id}`);
            } else {
                setInvalidRfid(rfid);
            }
        }

        const socket: Socket<ServerToClientEvents> = io(env.NEXT_PUBLIC_SOCKETIO_PORT)
        socket.on('zmq_rfid', onRfidEvent);

        return () => {
            socket.disconnect();
            socket.off('zmq_rfid', onRfidEvent);
        }
    }
    , [router]);

    return (
        <div className="text-sm p-3">
            {invalidRfid ? <h2 className="text-red-500 text-2xl">{`Invalid RFID: ${invalidRfid}`}</h2> : <h2 className="text-2xl">Please scan your item.</h2>}
        </div>
    )
}
