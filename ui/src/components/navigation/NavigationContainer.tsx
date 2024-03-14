'use client'

import { type NavigationState, type Product } from "@prisma/client"
import { useEffect, useState } from "react"
import { io, type Socket } from "socket.io-client"
import { env } from "~/env"
import { NavState, type NavMessages } from "~/types/Navigation"
import { cancelRoute } from "~/app/actions"
import NavigationInfoBar from "./NavigationInfoBar"
import NavigationMap from "./map/NavigationMap"


interface NavigationContainerProps {
    initialNavigationState: NavigationState | null;
    cartItems: Product[];
    getNavigationState: () => Promise<NavigationState | null>;
} 

interface ServerToClientEvents {
    zmq_navigation: (msg: NavMessages) => void;
}

interface ClientToServerEvents {
    ui_message: ({topic, msg}: {topic: string, msg: string}) => void;
}


export default function NavigationContainer({initialNavigationState, cartItems, getNavigationState}: NavigationContainerProps) {
    useEffect(() => {
        async function onNavEvent(msg: NavMessages) {
            console.log('Received nav event:', msg);
            setNavigationState(await getNavigationState());
        }

        const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(env.NEXT_PUBLIC_SOCKETIO_PORT)
        socket.on('zmq_navigation', onNavEvent);

        return () => {
            socket.disconnect();
            socket.off('zmq_navigation', onNavEvent);
        }
    }, [getNavigationState]);
    
    const [navigationState, setNavigationState] = useState<NavigationState | null>(initialNavigationState);

    function handleCancelRoute() {
        setNavigationState((prev) => {
            if (prev) {
                void cancelRoute();
                return {...prev, state: NavState.PENDING_CANCEL};
            }
            return null;
        })
    }

    return (
        <div className="flex flex-col h-screen space-y-1 bg-slate-300">
            <div className="bg-red-100 flex-1">
                <NavigationMap navigationState={navigationState!} cartItems={cartItems} />
            </div>
            <div className="bg-green-100">
                <NavigationInfoBar navigationState={navigationState!} handleCancelRoute={handleCancelRoute} />
            </div>
        </div>
    )
}
