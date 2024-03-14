import { type NavigationState } from '@prisma/client'

interface DestinationTextProps {
    navigationState: NavigationState
}

export default function NavigationDestinationText({navigationState}: DestinationTextProps) {
    return (
        <div className="text-2xl px-2">
            To: {navigationState.destName}
        </div>
    )
}
