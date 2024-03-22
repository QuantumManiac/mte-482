'use client'

import { type NavigationState } from "@prisma/client"

interface GuidanceTextProps {
    navigationState: NavigationState
}

export default function NavigationGuidanceText({navigationState}: GuidanceTextProps) {
    function determineNavigationTextAndIcon(): [string, string] {
        switch (navigationState.nextStep) {
            case "arrive_left":
                 return [`Destination on left in ${navigationState.distToNextStep?.toFixed(1)} m`, "🏁"]
            case "arrive_left":
                 return [`Destination on right in ${navigationState.distToNextStep?.toFixed(1)} m`, "🏁"]
            case "arrive":
                 return [`Destination in ${navigationState.distToNextStep?.toFixed(1)} m`, "🏁"]
            case "left":
                return [`Turn left in ${navigationState.distToNextStep?.toFixed(1)} m`, "⬅️"]
            case "right":
                return [`Turn right in ${navigationState.distToNextStep?.toFixed(1)} m`, "➡️"]
            default:
                return ["Currently Not Navigating", "💤"]
    }}

    const [navigationText, navigationIcon] = determineNavigationTextAndIcon()

    return (
        <div className="flex flex-row items-center w-full">
            <div className="text-2xl flex-1 px-2">
                {navigationText}
            </div>
            <div className="text-3xl px-2">
                {navigationIcon}
            </div>
        </div>
    )
}
