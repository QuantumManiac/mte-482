'use client';

import NavLink from "./NavLink";
import StatusBar from "./statusBar/StatusBar";

// Navbar is on right of the page

export default function Nav() {
    return (
        <div className="fixed top-0 right-0 h-screen bg-gray-800 flex flex-col justify-between w-32">
            <StatusBar/>
            <NavLink name="Home" path="/"/>
            <NavLink name="Items" path="/items"/>
            <NavLink name="Scan" path="/scan"/>
            <NavLink name="Navigate" path="/navigate"/> 
            {/* <NavLink name="Voice Assist"/>  */}
            {/* <NavLink name="Call for Help"/>  */}
        </div>
    );
    }
