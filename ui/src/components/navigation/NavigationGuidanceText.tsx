'use client'

import { type NavigationState } from "@prisma/client"

interface GuidanceTextProps {
    navigationState: NavigationState
}

export default function NavigationGuidanceText({navigationState}: GuidanceTextProps) {
    function determineNavigationTextAndIcon(): [string, string] {
        switch (navigationState.nextStep) {
            case "arrive":
                 return [`Destination in ${navigationState.distToNextStep} meters`, "🏁"]
            case "left":
                return [`Turn left in ${navigationState.distToNextStep} m`, "⬅️"]
            case "right":
                return [`Turn right in ${navigationState.distToNextStep} m`, "➡️"]
            default:
                return ["No Direction Provided", "❔"]
    }}

    const [navigationText, navigationIcon] = determineNavigationTextAndIcon()

    return (
        <div className="flex flex-row items-center">
            <div className="text-2xl flex-1 px-2">
                {navigationText}
            </div>
            <div className="text-3xl px-2">
                {navigationIcon}
            </div>
        </div>
    )
}