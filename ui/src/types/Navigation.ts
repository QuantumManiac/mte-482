export enum NavMessages {
    START_NAV = 'start_nav',
    CANCELLED = 'cancelled',
    RECALCULATED = 'recalculated',
    NEW_POSTION = 'new_position',
    MAKE_TURN = 'make_turn',
    ARRIVED = 'arrived',
}

export enum NavState {
    IDLE = 'idle',
    START_NAV = 'start_nav',
    NAVIGATING = 'navigating',
    PENDING_CANCEL = 'pending_cancel'
}
