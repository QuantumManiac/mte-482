'use client'

import { type NavigationState } from "@prisma/client"
import ActionButton from "../common/ActionButton"
import DashboardNavigationCompass from "./DashboardNavigationCompass"

interface DashboardNavigationProps {
    navigationState: NavigationState
    handleCancelRoute: () => void
}

export default function DashboardNavigation({navigationState, handleCancelRoute}: DashboardNavigationProps) {
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
    <div className="flex flex-col h-full w-full space-y-1">
        <div className="flex items-center bg-slate-100">
            <div className="text-2xl flex-1 px-2">
                To: {navigationState.destinationName}
            </div>
            <ActionButton style="bg-red-200" text="Cancel" icon="❌" onClick={() => handleCancelRoute()} />
        </div>
        <div className="bg-slate-100 flex-1">
            <DashboardNavigationCompass heading={navigationState.heading} desiredHeading={navigationState.desiredHeading} />
        </div>
        <div className="bg-slate-100">
            <div className="flex flex-row items-center">
                <div className="text-2xl flex-1 px-2">
                    {navigationText}
                </div>
                <div className="text-3xl px-2">
                    {navigationIcon}
                </div>
            </div>
        </div>
    </div>
    )
}
