from db import NavigationState, init_session
import enum
from time import sleep
import zmq
from sqlalchemy.orm.session import Session

# States that the navigation system can be in
class NavState(enum.Enum):
    IDLE = 'idle' # Not currently navigating
    START_NAV = 'start_nav' # Pending start of navigation
    NAVIGATING = 'navigating' # Currently navigating to a destination
    PENDING_CANCEL = 'pending_cancel' # Pending cancellation of navigation

# Messages to be sent to the UI
class NavMessages(enum.Enum):
    START_NAV = 'start_nav' # Navigation started to a new destination
    CANCELLED = 'cancelled' # Navigation was cancelled
    RECALCULATED = 'recalculated' # Route recalculated
    NEW_POSTION = 'new_position' # Position Updated (send new distance to next turn)
    MAKE_TURN = 'make_turn' # Make a turn
    ARRIVED = 'arrived' # Arrived at destination

# Update the current position of the cart to the database
def update_localization_state_to_db(session: Session, zmq_sub: zmq.Socket):
    try:
        _, msg = zmq_sub.recv_string(flags=zmq.NOBLOCK).split(' ', 1)
        x, y, heading = msg.split(',')
        with session.begin():
            session.query(NavigationState).filter(NavigationState.id == 0).update({NavigationState.currentX: x, NavigationState.currentY: y, NavigationState.heading: heading})
    except zmq.error.ZMQError:
        pass     
    
def calculate_route(session: Session, state: NavigationState, pub: zmq.Socket):
    # TODO Calculate route based on current position and destination
    # Get the destination from the database

    with session.begin():
        state.state = NavState.NAVIGATING
        # state.nextStep = 'left'
        # state.distToNextStep = 5
        # state.route = ...

    pub.send_string(f'zmq_navigation {NavMessages.START_NAV.value}')

def update_navigation_state(session: Session, state: NavigationState, pub: zmq.Socket):
    currentX, currentY, heading = state.currentX, state.currentY, state.heading
    # TODO Update state based on current position and route


    notification = NavMessages.NEW_POSTION # Or NavMessages.MAKE_TURN or NavMessages.ARRIVED, NavMessages.RECALCULATED implement this

    with session.begin():
        # TODO Update State
        # state.nextStep = 'left'
        # state.distToNextStep = 5
        # Also change the route if recalculated
        # state.route = ...
        pass

    pub.send_string(f'zmq_navigation {notification.value}')

def cancel_navigation(session: Session, state: NavigationState, pub: zmq.Socket):
    with session.begin():
        state.state = NavState.IDLE
        state.routeTo = None
        state.route = None
        state.nextStep = None
        state.distToNextStep = None
        
    pub.send_string(f'zmq_navigation {NavMessages.CANCELLED}')

def tick(session: Session, pub: zmq.Socket):
    with session.begin():
        state = session.query(NavigationState).filter(NavigationState.id == 0).first()

    match state.state:
        case NavState.IDLE:
            return
        case NavState.START_NAV:
            calculate_route(session, state, pub)
        case NavState.NAVIGATING:
            update_navigation_state(session, state, pub)
        case NavState.PENDING_CANCEL:
            cancel_navigation(session, pub)

def main():    
    context = zmq.Context()
    session = init_session()
    pub = context.socket(zmq.PUB)
    pub.connect("tcp://127.0.0.1:5556")

    sub: zmq.Socket = context.socket(zmq.SUB)
    sub.setsockopt(zmq.CONFLATE, 1)
    sub.connect("tcp://127.0.0.1:5555")
    sub.setsockopt(zmq.SUBSCRIBE, b"zmq_localization")

    # Create initial navigation state
    with session.begin():
        session.query(NavigationState).delete()
        session.add(NavigationState(id=0, state=NavState.IDLE))

    # Update state every 300ms
    while True:
        update_localization_state_to_db(session, sub)
        tick(session, pub)
        sleep(0.3)

    







 

    







if __name__ == "__main__":
    main()
