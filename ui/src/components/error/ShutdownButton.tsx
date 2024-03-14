'use client'

import { io, type Socket } from "socket.io-client";

import { env } from "~/env";

import ActionButton from "~/components/common/ActionButton";

export default function ShutdownButton() {
  const socket: Socket = io(env.NEXT_PUBLIC_SOCKETIO_PORT);

  function sendShutdownMessage() {
    socket.emit('shutdown', {topic: 'shutdown', msg: 'shutdown'});
  }

  return (
      <ActionButton style="flex bg-red-950 text-white" icon="❌" text="Shutdown" onClick={() => sendShutdownMessage()} />
  );
}