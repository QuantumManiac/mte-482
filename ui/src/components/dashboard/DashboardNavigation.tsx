'use client'

import { type NavigationState } from "@prisma/client"
import ActionButton from "../common/ActionButton"
import NavigationCompass from "../navigation/NavigationCompass"
import NavigationGuidanceText from "../navigation/NavigationGuidanceText"
import NavigationDestinationText from "../navigation/NavigationDestinationText"

interface DashboardNavigationProps {
    navigationState: NavigationState
    handleCancelRoute: () => void
}

export default function DashboardNavigation({navigationState, handleCancelRoute}: DashboardNavigationProps) {
    return (
    <div className="flex flex-col h-full w-full space-y-1">
        <div className="flex items-center bg-slate-100">
            <div className="flex-1">
                <NavigationDestinationText navigationState={navigationState} />
            </div>
            <ActionButton style="bg-red-200" text="Cancel" icon="❌" onClick={() => handleCancelRoute()} />
        </div>
        <div className="bg-slate-100 flex-1">
            <NavigationCompass heading={navigationState.heading} desiredHeading={navigationState.desiredHeading} />
        </div>
        <div className="bg-slate-100">
            <NavigationGuidanceText navigationState={navigationState} />
        </div>
    </div>
    )
}
