import { type NavigationState } from "@prisma/client"

interface DashboardNavigationProps {

    navigationState: NavigationState
}

export default function DashboardNavigation({navigationState}: DashboardNavigationProps) {
    return (
        <div className="flex flex-col">
            <h1 className="text-3xl font-bold">Navigation</h1>
            <p className="text-2xl font-bold">{navigationState.currentX}</p>
            <p className="text-2xl font-bold">{navigationState.currentY}</p>
            <p className="italic mt-auto text-slate-500">ID: {navigationState.id}</p>
        </div>
    )
}
