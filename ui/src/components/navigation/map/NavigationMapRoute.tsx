import { type Coordinate } from "~/types/Navigation"
import { type NavigationState } from "@prisma/client"
import MapMarker from "./MapMarker"

interface NavigationMapRouteProps {
    navigationState: NavigationState,
    transformCoordinate: (x: number, y: number) => Coordinate
}


export default function NavigationMapRoute({navigationState, transformCoordinate}: NavigationMapRouteProps) {
    const pathString = navigationState.route

    function parsePathString(pathString: string | null): Coordinate[]  {
        if (!pathString) {
            return []
        }

        const routeSegments = pathString.split('|')
        const res = routeSegments.map((segment) => {
            const [x, y, _] = segment.split(',')
            return {x: parseFloat(x!), y: parseFloat(y!)}
        })

        return res
    }

    function generatePath(path: Coordinate[]): JSX.Element {
        path = path.map((coord): Coordinate => transformCoordinate(coord.x, coord.y))
        if (path.length < 2) {
            return <></>
        } else {
            // Start the 'd' attribute with the 'M' command to move to the first point
            let d = `M ${path[0]!.x},${path[0]!.y}`;

            // Append 'L' commands to draw lines to each subsequent point
            for (let i = 1; i < path.length; i++) {
                d += ` L ${path[i]!.x},${path[i]!.y}`;
            }

            const lastPoint = path[path.length - 1]!;

            // Return the SVG element with the path
            return (
                <>
                    <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                        <path d={d} stroke="#86efac" strokeWidth={10} fill="none" />
                    </svg>
                    <MapMarker pos={{x: lastPoint.x, y: lastPoint.y}} icon="🏁" tooltipText={navigationState.destName} />
                </>
            );
        }
    }

    return (
        <div className="h-full w-full">
            {generatePath(parsePathString(pathString))}
        </div>
    )
}
