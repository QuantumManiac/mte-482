import NavLink from "./NavLink";
import StatusBar from "./StatusBar";

// Navbar is on right of the page
export default function Nav() {
    return (
        <div className="fixed top-0 right-0 h-screen bg-gray-800 flex flex-col justify-between w-32">
            <StatusBar/>
            <NavLink/>
            <NavLink/>
            <NavLink/>
            <NavLink/> 
            <NavLink/> 
            <NavLink/> 
        </div>
    );
    }
