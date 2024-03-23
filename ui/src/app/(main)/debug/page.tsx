'use client'

import { useEffect, useState } from 'react'
import { io, type Socket } from 'socket.io-client'
import { env } from '~/env'

import type IMUData from '~/types/IMUData'
import type ADCData from '~/types/ADCData'

interface ServerToClientEvents {
    battery_voltage: (b: number) => void
    push_assist: (b: boolean) => void
    rfid: (b: string) => void
    imu: (b: IMUData) => void
    adc: (b: ADCData) => void
}

interface ClientToServerEvents {
    ui_message: ({topic, msg}: {topic: string, msg: string}) => void
}

export default function Page() {
    const [battery, setBattery] = useState<number | undefined>(undefined)
    const [assist, setAssist] = useState<boolean | undefined>(undefined)
    const [rfid, setRfid] = useState<string | undefined>(undefined)
    const [imu, setImu] = useState<IMUData | undefined>(undefined)
    
    useEffect(() => {
        function onBatteryEvent(battery: number) {
            setBattery(battery)
        }
        function onAssistEvent(assist: boolean) {
            setAssist(assist)
        }
        function onRfidEvent(rfid: string) {
            setRfid(rfid)
        }
        function onImuEvent(imu: IMUData) {
            setImu(imu)
        }

        const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(env.NEXT_PUBLIC_SOCKETIO_PORT)
        console.log("Connected to socket.io server")
        socket.on('battery_voltage', onBatteryEvent)
        socket.on('push_assist', onAssistEvent)
        socket.on('rfid', onRfidEvent)
        socket.on('imu', onImuEvent)

        return () => {
            socket.disconnect()
            socket.off('battery_voltage', onBatteryEvent)
            socket.off('push_assist', onAssistEvent)
            socket.off('rfid', onRfidEvent)
            socket.off('imu', onImuEvent)
        }
    }
    , [])
    return (
        <main>
            <h1>Battery Voltage: {battery ?? "???"}</h1>
            <h1>Assist: {assist ?? "???"}</h1>
            <h1>Rfid: {rfid ?? "???"}</h1>
            <h1>Imu: {imu?.accel_x ?? "???"}, {imu?.accel_y ?? "???"}, {imu?.accel_z ?? "???"}</h1>
        </main>
    );
} 
