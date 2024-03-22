from db import NavigationState, init_session
import enum
from time import sleep
import zmq
from sqlalchemy.orm.session import Session
import navigation_old as navigation
from typing import List

TILES_X = 39
TILES_Y = 21
SCALE_X = 1
SCALE_Y = 1

grid = navigation.make_grid(TILES_X, TILES_Y, SCALE_X, SCALE_Y)
navigation.make_set_barrier(grid)
path: List[navigation.Point] = []
directions = []


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

def dist_calc(curr_x, curr_y, next_x, next_y):
    return abs(curr_x*SCALE_X - next_x*SCALE_X) + abs(curr_y*SCALE_Y - next_y*SCALE_Y)

# Update the current position of the cart to the database
def update_localization_state_to_db(session: Session, zmq_sub: zmq.Socket):
    try:
        _, msg = zmq_sub.recv_string(flags=zmq.NOBLOCK).split(' ', 1)
        x, y, heading = msg.split(',')
        with session.begin():
            session.query(NavigationState).filter(NavigationState.id == 0).update({NavigationState.currentX: x, NavigationState.currentY: y, NavigationState.heading: heading})
            session.commit()
    except zmq.error.ZMQError:
        pass     

def find_heading(curr_x, curr_y, end_x, end_y):
    heading = 0
    if curr_y < end_y:
        heading = 180
    elif curr_x < end_x:
        heading = 90
    elif curr_x > end_x:
        heading = 270

    return heading

def des_loc(start_x, start_y, end_x, end_y, heading):
    direction = ""
    des_heading = 0
    des_heading = find_heading(start_x, start_y, end_x, end_y)
    if des_heading != heading:
        if des_heading == 0:
            if heading <= 180:
                direction = "right"
            else:
                direction = "left"
        elif des_heading == 90:
            if heading > 90 and heading <= 270:
                direction = "right"
            else:
                direction = "left"
        elif des_heading == 180:
            if heading > 180 and heading < 360:
                direction = "right"
            else:
                direction = "left"
        elif des_heading == 270:
            if heading < 90 and heading > 270:
                direction = "right"
            else:
                direction = "left"
    else:
        direction = "straight"

    return direction, des_heading


    
def calculate_route(session: Session, state: NavigationState, pub: zmq.Socket):
    global path
    global directions
    next_step = ''
    complete = False
    dist_to_next = 0
    heading = 0
    start_x, start_y, end_x, end_y = int(round(state.currentX)), int(round(state.currentY)), int(round(state.destX)), int(round(state.destY))
    start = grid[start_x][start_y]
    start.make_start()
    end = grid[end_x][end_y]
    end.make_end()

    dist_to_next = dist_calc(start_x, start_y, end_x, end_y)

    if dist_to_next == 1:
        next_step, heading = des_loc(start_x, start_y, end_x, end_y, state.heading)
        path_str = next_step
    else: 
        complete, path, path_str, directions = navigation.algorithm(grid, start, end)
        heading = 0


    if complete:
        next_step = directions[0]
        dist_to_next = dist_calc(start_x, start_y, path[0].x, path[0].y)
        heading = find_heading(start_x, start_y, path[0].x, path[0].y)

    state.state = NavState.NAVIGATING.value
    # state.nextStep = 'left'
    state.nextStep = next_step
    # state.distToNextStep = 5
    state.distToNextStep = dist_to_next
    # state.desiredHeading = 180
    state.desiredHeading = heading
    # state.route = ...
    state.route = path_str

    print(f'Starting navigation. Route: {path_str}')

    pub.send_string(f'zmq_navigation {NavMessages.START_NAV.value}')

def to_recalculate(curr, next):
    if navigation.pythagorean(curr, next) > navigation.h(curr, next):
        return True
    
    return False


def update_navigation_state(session: Session, state: NavigationState, pub: zmq.Socket):
    global path
    global directions
    currentX, currentY, end_x, end_y, heading = int(round(state.currentX)), int(round(state.currentY)), int(round(state.destX)), int(round(state.destY)), int(round(state.heading))
    # TODO Update state based on current position and route
    notification = NavMessages.NEW_POSTION # Or NavMessages.MAKE_TURN or NavMessages.ARRIVED, NavMessages.RECALCULATED implement this

    if ((currentX, currentY) == (end_x, end_y)):
        notification = NavMessages.ARRIVED
    else:
        curr_pos = [(currentX), (currentY)]
        next_turn = [(path[0].y), (path[0].x)]
        recalculate = to_recalculate(curr_pos, next_turn)
        dist_to_next = dist_calc(currentX, currentY, path[0].x, path[0].y)

        if recalculate:
            start = grid[currentX][currentY]
            end = grid[end_x][end_y]
            complete, path, path_str, directions = navigation.algorithm(grid, start, end)
            print(f'Recalculated route: {path_str}')
            notification = NavMessages.RECALCULATED
        elif dist_to_next <= 2: #may pose an issue if the user turns too quickly:,)
            directions.pop(0)
            curr_pos = [path[0].y, path[0].x]
            path.pop(0)
            dist_to_next = dist_calc(currentX, currentY, path[0].x, path[0].y)
            print(f'Making turn: {directions[0]}')
            notification = NavMessages.MAKE_TURN
            
        heading = find_heading(currentX, currentY, path[0].x, path[0].y)

        # TODO Update State
        # state.nextStep = 'left'
        state.nextStep = directions[0]
        # state.distToNextStep = 5
        state.distToNextStep = dist_to_next
        # state.desiredHeading = 5
        state.desiredHeading = heading
        # Also change the route if recalculated
        # state.route = ...
        if notification == NavMessages.RECALCULATED:
            state.route = path_str

        pub.send_string(f'zmq_navigation {notification.value}')

def cancel_navigation(session: Session, state: NavigationState, pub: zmq.Socket):
    state.state = NavState.IDLE.value
    state.routeTo = None
    state.route = None
    state.nextStep = None
    state.distToNextStep = None
    print('Navigation cancelled')
        
    pub.send_string(f'zmq_navigation {NavMessages.CANCELLED}')

def tick(session: Session, pub: zmq.Socket):
    state = session.query(NavigationState).filter(NavigationState.id == 0).first()
    session.commit()

    match state.state:
        case NavState.IDLE.value:
            return
        case NavState.START_NAV.value:
            calculate_route(session, state, pub)
        case NavState.NAVIGATING.value:
            update_navigation_state(session, state, pub)
        case NavState.PENDING_CANCEL.value:
            cancel_navigation(session, state, pub)

def main():    
    context = zmq.Context()
    session = init_session()
    pub = context.socket(zmq.PUB)
    pub.connect("tcp://127.0.0.1:5556")

    sub: zmq.Socket = context.socket(zmq.SUB)
    sub.setsockopt(zmq.CONFLATE, 1)
    sub.connect("tcp://127.0.0.1:5555")
    sub.setsockopt(zmq.SUBSCRIBE, b"zmq_localization")

    with session.begin():
        session.query(NavigationState).delete()
        session.add(NavigationState(id=0, currentX=1, currentY=1, state=NavState.IDLE.value))
        session.commit()

    # Update state every 300ms
    while True:
        update_localization_state_to_db(session, sub)
        tick(session, pub)
        sleep(0.3)
        # sleep(1)

if __name__ == "__main__":
    main()
