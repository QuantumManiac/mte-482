import NavigationGuidanceText from "./NavigationGuidanceText"
import { type NavigationState } from "@prisma/client"
import { NavState } from "~/types/Navigation"
import NavigationDestinationText from "./NavigationDestinationText"
import ActionButton from "../common/ActionButton"

interface NavigationInfoBarProps {
    navigationState: NavigationState
    handleCancelRoute: () => void
}

export default function NavigationInfoBar({navigationState, handleCancelRoute}: NavigationInfoBarProps) {
    if (navigationState.state as NavState != NavState.NAVIGATING) {
        return (
            <div className="flex flex-col items-center justify-center h-[4rem] bg-slate-200">
                <p className="text-2xl font-bold text-slate-600">Currently Not Navigating</p>
            </div>
        )
    } else {
        return (
            <div className="flex space-x-1 bg-slate-300 h-[5rem]">
                <div className="flex-1 flex items-center bg-slate-100 h-full">
                    <NavigationDestinationText navigationState={navigationState} />
                </div>
                <ActionButton style="bg-red-200" text="Cancel" icon="❌" onClick={() => handleCancelRoute()} />
                <div className="flex-1 flex bg-slate-100 h-full items-center">
                    <NavigationGuidanceText navigationState={navigationState} />
                </div>
            </div>
        )
    }
    
}
