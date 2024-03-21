from db import NavigationState, init_session
from time import sleep

session = init_session()

def update_state(vals: dict):
    with session.begin():
        state = session.query(NavigationState).filter(NavigationState.id == 0).first()
        for k, v in vals.items():
            setattr(state, k, v)
        session.commit()
print("############################")
print("Emulate localization updates and navigation commands")
print("Commands:")
print("start x,y - start navigation to location x,y")
print("cancel - cancel navigation")
print("enter in a coordinate in the form x,y to emulate a location update")
print("can also enter in a coordinate and heading x,y,heading to emulate a location update with a heading (heading is 0-359)")
print("############################")
while True:
    with session.begin():
        state = session.query(NavigationState).filter(NavigationState.id == 0).first()
        print(f"Current state: {state.state}, current location: ({state.currentX},{state.currentY} (heading {state.heading}))")
        if state.state != "idle":
            print(f"Route: {state.route}")
            print(f"Next step: {state.nextStep} in {state.distToNextStep} m (head {state.desiredHeading}) | destination: ({state.destX},{state.destY})")
    action = input("Enter command: ")

    if action.startswith("start"):
        x, y = action.split(" ")[1].split(",")
        x, y = int(x), int(y)
        print(f"Requesting start navigation to {x},{y}")
        update_state({
            "destX": x,
            "destY": y,
            "state": "start_nav"
        })

    elif action == "cancel":
        print("Requesting cancel navigation")
        update_state({
            "state": "pending_cancel"
        })

    elif "," in action:
        args = action.split(",") 
        if len(args) == 2:
            x, y = args
            print(f"Emulating location update to {x},{y}")
            update_state({
                "currentX": x,
                "currentY": y
            })
        elif len(args) == 3:
            x, y, heading = args
            print(f"Emulating location update to {x},{y} with heading {heading}")
            update_state({
                "currentX": x,
                "currentY": y,
                "heading": heading
            })
    else:
        print("Invalid command")
        continue
    
    sleep(1)
