import BatteryIndicator from "./BatteryIndicator";

export default function StatusBar() {
    return (
        <div className="border text-white border-white text-sm p-3">
            <BatteryIndicator/>
        </div>
    )
}
