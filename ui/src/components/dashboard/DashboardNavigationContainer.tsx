'use client'

import { type NavigationState } from "@prisma/client";
import { useEffect, useState } from "react";
import { io, type Socket } from "socket.io-client";
import { env } from "~/env"
import { type NavMessages, NavState } from "~/types/Navigation";

import { cancelRoute } from "~/app/actions";

import DashboardNavigation from "./DashboardNavigation";
import { revalidatePath } from "next/cache";


interface DashboardNavigationContainerProps {
    initialNavigationState: NavigationState | null;
    getNavigationState: () => Promise<NavigationState | null>;
}

interface ServerToClientEvents {
    zmq_navigation: (msg: NavMessages) => void;
}

interface ClientToServerEvents {
    ui_message: ({topic, msg}: {topic: string, msg: string}) => void;
}

export default function DashboardNavigationContainer({ initialNavigationState, getNavigationState }: DashboardNavigationContainerProps) {
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

    switch (navigationState ? navigationState.state : null as NavState | null) {
        case NavState.IDLE:
            return (
                <div className="flex flex-col items-center justify-center h-full bg-slate-200">
                    <p className="text-2xl font-bold text-slate-600">Currently Not Navigating</p>
                </div>
            )
        case NavState.START_NAV:
            return (
                <div className="flex flex-col items-center justify-center h-full bg-green-100">
                    <p className="text-2xl font-bold animate-pulse text-slate-600">Starting Navigation...</p>
                </div>
            )
        case NavState.PENDING_CANCEL:
            return (
                <div className="flex flex-col items-center justify-center h-full bg-red-100">
                    <p className="text-2xl font-bold animate-pulse text-slate-600">Cancelling Route...</p>
                </div>
            )
        case NavState.NAVIGATING:
            return (
                <div className="flex flex-col items-center justify-center h-full bg-slate-300">
                    <DashboardNavigation navigationState={navigationState!} handleCancelRoute={handleCancelRoute}/>
                </div>
            )
        default:
            return (
                <div className="flex flex-col items-center justify-center h-full bg-slate-200">
                    <p className="text-2xl font-bold animate-pulse text-slate-600">Loading...</p>
                </div>
            )
    }
}
