from db import NavigationState, init_session
import enum
from time import sleep
import zmq
from sqlalchemy.orm.session import Session
import navigation_old as navigation

GRID = navigation.make_grid(40, 600)
path = []
dir = []
SCALE = 50

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

COORDINATE_TRANSFORM_FACTOR = 300

# Update the current position of the cart to the database
def update_localization_state_to_db(session: Session, zmq_sub: zmq.Socket):
    try:
        _, msg = zmq_sub.recv_string(flags=zmq.NOBLOCK).split(' ', 1)
        x, y, heading = msg.split(',')
        state = session.query(NavigationState).filter(NavigationState.id == 0).first()
        state.currentX = float(x) * COORDINATE_TRANSFORM_FACTOR
        state.currentY = float(y) * COORDINATE_TRANSFORM_FACTOR
        state.heading = float(heading)
        session.commit()

    except zmq.error.ZMQError:
        pass     
    
def calculate_route(session: Session, state: NavigationState, pub: zmq.Socket):
    # TODO Calculate route based on current position and destination
    next_step = ''
    dist_to_next = 0
    heading = 0
    start_x, start_y, end_x, end_y = state.currentX, state.currentY, state.destX, state.destY
    start = GRID[start_x][start_y]
    end = GRID[end_x][end_y]
    print("start")
    complete, path, path_str, dir = navigation.algorithm(GRID, start, end)
    heading = 0
    # Get the destination from the database

    if complete:
        next_step = dir[0]
        # next_x, next_y = path[0][0], path[0][1]
        dist_to_next = navigation.h(path[0], start)
        if start_x > path[0][0]:
            heading = 180
        elif start_y < path[0][1]:
            heading = 270
        else:
            heading = 360

    state.state = NavState.NAVIGATING.value
    # state.nextStep = 'left'
    state.nextStep = next_step
    # state.distToNextStep = 5
    state.distToNextStep = dist_to_next
    # state.desiredHeading = 180
    state.desiredHeading = heading
    # state.route = ...
    state.route = path_str

    pub.send_string(f'navigation {NavMessages.START_NAV.value}')

def to_recalculate(curr, next):
    if navigation.pythagorean(curr, next) > navigation.h(curr, next):
        return True
    
    return False


def update_navigation_state(session: Session, state: NavigationState, pub: zmq.Socket):
    currentX, currentY, heading = state.currentX, state.currentY, state.heading
    # TODO Update state based on current position and route

    notification = NavMessages.NEW_POSTION # Or NavMessages.MAKE_TURN or NavMessages.ARRIVED, NavMessages.RECALCULATED implement this
    
    heading = 0
    curr_pos = [(currentX), (currentY)]
    next_turn = path[0]
    recalculate = to_recalculate(curr_pos, next_turn)
    dist_to_next = navigation.h(curr_pos, next_turn)

    if (currentX, currentY == state.destX, state.destY):
        notification = NavMessages.ARRIVED
    elif recalculate:
        start = GRID[currentX][currentY]
        end = GRID[state.destX][state.destY]
        complete, path, path_str, dir = navigation.algorithm(GRID, start, end)
        notification = NavMessages.RECALCULATED
    elif dist_to_next <= 2: #may pose an issue if the user turns too quickly:,)
        dir.pop(0)
        curr_pos = [path[0][0], path[0][1]]
        path.pop(0)
        dist_to_next = navigation.h(curr_pos, next_turn) * SCALE
        notification = NavMessages.MAKE_TURN

    if currentX > path[0][0]:
        heading = 180
    elif currentY < path[0][1]:
        heading = 270
    else:
        heading = 360

    # TODO Update State
    # state.nextStep = 'left'
    state.nextStep = dir[0]
    # state.distToNextStep = 5
    state.distToNextStep = dist_to_next
    # state.desiredHeading = 5
    state.desiredHeading = heading
    # Also change the route if recalculated
    # state.route = ...
    if notification == NavMessages.RECALCULATED:
        state.route = path_str
    pass

    pub.send_string(f'navigation {notification.value}')

def cancel_navigation(session: Session, state: NavigationState, pub: zmq.Socket):
    state.state = NavState.IDLE.value
    state.routeTo = None
    state.route = None
    state.nextStep = None
    state.distToNextStep = None
        
    pub.send_string(f'navigation {NavMessages.CANCELLED}')

def tick(session: Session, pub: zmq.Socket):
    state = session.query(NavigationState).filter(NavigationState.id == 0).first()
    print(state.state)
    match state.state:
        case NavState.IDLE.value:
            pub.send_string(f'navigation {NavMessages.NEW_POSTION}')
        case NavState.START_NAV.value:
            print("Start nav")
            calculate_route(session, state, pub)
        case NavState.NAVIGATING.value:
            update_navigation_state(session, state, pub)
        case NavState.PENDING_CANCEL.value:
            print("Pending cancel")
            cancel_navigation(session, pub)

def main():    
    print("Starting navigation process...")
    context = zmq.Context()
    session = init_session()
    pub = context.socket(zmq.PUB)
    pub.connect("tcp://127.0.0.1:5556")

    sub: zmq.Socket = context.socket(zmq.SUB)
    sub.setsockopt(zmq.CONFLATE, 1)
    sub.connect("tcp://127.0.0.1:5555")
    sub.setsockopt(zmq.SUBSCRIBE, b"localization")

    # Create initial navigation state
    with session.begin():
        session.query(NavigationState).delete()
        session.add(NavigationState(id=0, state=NavState.IDLE.value))
    # Update state every 300ms
    while True:
        update_localization_state_to_db(session, sub)
        tick(session, pub)
        sleep(0.3)

    







 

    







if __name__ == "__main__":
    main()
