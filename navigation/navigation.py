from db import NavigationState, init_session
import enum
from time import sleep, time
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
is_barrier = False


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
def update_localization_state_to_db(zmq_sub: zmq.Socket):
    try:
        _, msg = zmq_sub.recv_string(flags=zmq.NOBLOCK).split(' ', 1)
        x, y, heading = msg.split(',')
        session = init_session()
        with session.begin():
            session.query(NavigationState).filter(NavigationState.id == 0).update({NavigationState.currentX: x, NavigationState.currentY: y, NavigationState.heading: heading})
            session.commit()
    except zmq.error.ZMQError:
        pass     
    except Exception as e:
        print(f"{time()} Failed. Trying again.")

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
                direction = "left"
            else:
                direction = "right"
        elif des_heading == 90:
            if heading > 90 and heading <= 270:
                direction = "left"
            else:
                direction = "right"
        elif des_heading == 180:
            if heading > 180 and heading < 360:
                direction = "left"
            else:
                direction = "right"
        elif des_heading == 270:
            if heading < 90 and heading > 270:
                direction = "left"
            else:
                direction = "right"
    else:
        direction = "straight"

    return direction, des_heading

def calculate_route(state: NavigationState, pub: zmq.Socket):
    navigation.make_set_barrier(grid)
    global path
    global directions
    global is_barrier
    next_step = ''
    complete = False
    dist_to_next = 0
    heading = 0
    start_x, start_y, end_x, end_y = int(round(state.currentX)), int(round(state.currentY)), int(round(state.destX)), int(round(state.destY))
    start = grid[start_x][start_y]
    start.make_start()
    end = grid[end_x][end_y]
    is_barrier = end.is_barrier()
    end.make_end()

    dist_to_next = dist_calc(start_x, start_y, end_x, end_y)

    if dist_to_next <= 1:
        next_step, heading = des_loc(start_x, start_y, end_x, end_y, state.heading)
        end = grid[end_x][end_y]
        # is_barrier = end.is_barrier()
        end.make_end()
        if not(is_barrier):
            path.append(end)
            directions = next_step
            path_str = next_step
        else:
            dist_to_next = 0
            directions = next_step
            path_str = "arrived_" + next_step
    else: 
        complete, path, path_str, directions = navigation.algorithm(grid, start, end, is_barrier)
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

    pub.send_string(f'navigation {NavMessages.START_NAV.value}')

def to_recalculate(prev, curr, next):
    if ((navigation.pythagorean(curr, prev) > 3) or (navigation.pythagorean(curr, next) < navigation.h(curr, next))):
        return True
    
    return False


def update_navigation_state(state: NavigationState, pub: zmq.Socket):
    global path
    global directions
    global is_barrier
    next_step = ""
    dist_to_next = 0
    currentX, currentY, end_x, end_y, heading = int(round(state.currentX)), int(round(state.currentY)), int(round(state.destX)), int(round(state.destY)), int(round(state.heading))
    # TODO Update state based on current position and route
    notification = NavMessages.NEW_POSTION # Or NavMessages.MAKE_TURN or NavMessages.ARRIVED, NavMessages.RECALCULATED implement this

    if ((currentX, currentY) == (end_x, end_y)):
        notification = NavMessages.ARRIVED
        dist_to_next = 0
        state.nextStep = "Arrived"
        # state.distToNextStep = 5
        state.distToNextStep = dist_to_next
        path = []
    else:
        # curr_pos = [(currentX), (currentY)]
        # next_turn = [(path[0].y), (path[0].x)]
        recalculate = False
        if len(path) > 0:
            dist_to_next = dist_calc(currentX, currentY, path[0].x, path[0].y)
            if state.distToNextStep < dist_to_next and (dist_to_next != 0):
                recalculate = True
        
        # recalculate = to_recalculate(prev_pos, curr_pos, next_turn)

        if recalculate:
            navigation.make_set_barrier(grid)
            start = grid[currentX][currentY]
            start.make_start()
            end = grid[end_x][end_y]
            is_barrier = end.is_barrier()
            end.make_end()
            complete, path, path_str, directions = navigation.algorithm(grid, start, end, is_barrier)
            print(f'Recalculated route: {path_str}')
            notification = NavMessages.RECALCULATED
        elif dist_to_next <= 0: #may pose an issue if the user turns too quickly:,)
            # curr_pos = [path[0].x, path[0].y]
            if (len(path) > 0):
                dist_to_next = dist_calc(currentX, currentY, path[0].x, path[0].y)
                # print(f'path[0]: {path[0].x}, {path[0].y}')
                # print(f'path len: {len(path)}')
                path.pop(0)
                print(f'Making turn: {directions[0]}')
                directions.pop(0)
                notification = NavMessages.MAKE_TURN
        
        if (len(path) == 0 and is_barrier):
            heading = find_heading(currentX, currentY, end_x, end_y)
            next_step = "Arrived"
        elif (len(path) == 0 and not(is_barrier)):
            heading = state.desiredHeading
            next_step = "Arrived"
        else:
            heading = find_heading(currentX, currentY, path[0].x, path[0].y)
            next_step = directions[0]
            

        # TODO Update State
        # state.nextStep = 'left'
        state.nextStep = next_step
        # state.distToNextStep = 5
        state.distToNextStep = dist_to_next
        # state.desiredHeading = 5
        state.desiredHeading = heading
        # Also change the route if recalculated
        # state.route = ...
        if notification == NavMessages.RECALCULATED:
            state.route = path_str

        pub.send_string(f'navigation {notification.value}')

def cancel_navigation(state: NavigationState, pub: zmq.Socket):

    state.state = NavState.IDLE.value
    state.route = None
    state.nextStep = None
    state.distToNextStep = None

    print('Navigation cancelled')
        
    pub.send_string(f'navigation {NavMessages.CANCELLED}')

def send_new_pos(pub: zmq.Socket):
    pub.send_string(f'navigation {NavMessages.NEW_POSTION.value}')

def tick(pub: zmq.Socket):
    session = init_session()
    state = session.query(NavigationState).filter(NavigationState.id == 0).first()

    match state.state:
        case NavState.IDLE.value:
            send_new_pos(pub)
        case NavState.START_NAV.value:
            calculate_route(state, pub)
        case NavState.NAVIGATING.value:
            # calculate_route(state, pub)
            update_navigation_state(state, pub)
        case NavState.PENDING_CANCEL.value:
            cancel_navigation(state, pub)

    session.commit()

def main():    
    context = zmq.Context()
    pub = context.socket(zmq.PUB)
    pub.connect("tcp://127.0.0.1:5556")

    sub: zmq.Socket = context.socket(zmq.SUB)
    sub.setsockopt(zmq.CONFLATE, 1)
    sub.connect("tcp://127.0.0.1:5555")
    sub.setsockopt(zmq.SUBSCRIBE, b"localization")

    session = init_session()
    with session.begin():
        session.query(NavigationState).delete()
        session.add(NavigationState(id=0, currentX=1, currentY=1, state=NavState.IDLE.value))
        session.commit()

    print("Starting navigation process...")

    # Update state every 300ms
    while True:
        update_localization_state_to_db(sub)
        tick(pub)
        sleep(0.3)
        # sleep(1)

if __name__ == "__main__":
    main()