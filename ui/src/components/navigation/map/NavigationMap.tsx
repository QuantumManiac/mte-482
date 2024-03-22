import { type NavigationState, type Product } from "@prisma/client"
import MapMarker from "./MapMarker"
import CartMarker from "./CartMarker"
import { NavState, type Coordinate } from "~/types/Navigation"
import NavigationMapRoute from "./NavigationMapRoute"

interface NavigationMapProps {
    navigationState: NavigationState
    cartItems: Product[]
}

export default function NavigationMap({navigationState, cartItems}: NavigationMapProps) {

    
    const transformCoordinate = (x: number, y: number): Coordinate => {
        // Tile size is 39x21. Image size is 1152x652
        const X_SCALE = 1152 / 39
        const Y_SCALE = 652 / 21
        const X_OFFSET = X_SCALE / 2
        const Y_OFFSET = Y_SCALE / 2
        return {
            x: x * X_SCALE + X_OFFSET,
            y: y * Y_SCALE + Y_OFFSET
        }
    }
    
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
            {navigationState.route && <NavigationMapRoute pathString={navigationState.route} transformCoordinate={transformCoordinate} />}
            <CartMarker pos={transformCoordinate(navigationState.currentX, navigationState.currentY)} heading={navigationState.heading}/>
            {displayDest && <MapMarker pos={transformCoordinate(navigationState.destX!, navigationState.destY!)} icon="🏁" tooltipText={navigationState.destName} />}
            {cartItems.map((item, index) => {
                if (item.locationX && item.locationY) {
                    const isDestination = navigationState.destX == item.locationX && navigationState.destY == item.locationY;
                    if (isDestination) {
                        return
                    }
                    const icon = item.done ? "✅" : "🚩"
                    return <MapMarker key={index} pos={transformCoordinate(item.locationX, item.locationY)} icon={icon} tooltipText={item.name} />
                }
            })}
        </div>
    )
}
