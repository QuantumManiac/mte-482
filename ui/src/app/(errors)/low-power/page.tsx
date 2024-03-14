import ShutdownButton from "~/components/error/ShutdownButton";
import StatusBar from "~/components/nav/statusBar/StatusBar";

export default function Page() {
    




    return (
        <div className="bg-zinc-900 flex flex-col h-full">
            <div className="flex">
                <ShutdownButton/>
                <div className="flex-1"/>
                <div className="flex right-0">
                    <StatusBar />           
                </div>
            </div>
            <div className="flex-1">
                <div className="flex flex-col justify-center items-center h-full">
                    <h1 className="text-4xl text-white">Low Battery</h1>
                    <p className="text-white">Please safely shut down the power and charge the battery.</p>
                </div>
            </div>
        </div>
    );
}