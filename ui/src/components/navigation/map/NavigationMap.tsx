import { type NavigationState, type Product } from "@prisma/client"
import MapMarker from "./MapMarker"
import CartMarker from "./CartMarker"
import { NavState } from "~/types/Navigation"

interface NavigationMapProps {
    navigationState: NavigationState
    cartItems: Product[]
}

export default function NavigationMap({navigationState, cartItems}: NavigationMapProps) {
    const displayDest = navigationState.state as NavState == NavState.NAVIGATING && navigationState.destX && navigationState.destY
    const mapStyle = {
        backgroundImage: "url('/img/map.png')",
        backgroundSize: "100% 100%",
        backgroundRepeat: "no-repeat",
        height: '100%',
        width: '100%',
        flex: 1,
  };
    return (
        <div style={mapStyle}>
            <CartMarker x={navigationState.currentX} y={navigationState.currentY} heading={navigationState.heading}/>
            {displayDest && <MapMarker x={navigationState.destX!} y={navigationState.destY!} icon="🏁" tooltipText={navigationState.destName} />}
            {cartItems.map((item, index) => {
                if (item.locationX && item.locationY) {
                    const isDestination = navigationState.destX == item.locationX && navigationState.destY == item.locationY;
                    if (isDestination) {
                        return
                    }
                    const icon = item.done ? "✅" : "🚩"
                    return <MapMarker key={index} x={item.locationX} y={item.locationY} icon={icon} tooltipText={item.name} />
                }
            })}
        </div>
    )
}
