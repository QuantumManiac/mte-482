export default async function Home() {
    return (
      <div className="flex space-x-1 bg-slate-300">
        <div className="flex-1 h-screen bg-red-100">
          Items
        </div>
        <div className="flex-1 h-screen bg-green-100">
          Map
        </div>
      </div>
    );
}
