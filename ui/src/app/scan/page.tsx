import ScanListener from "~/components/scan/ScanListener";
import { db } from "~/server/db";

export default async function Page() {


  return (
    <main className="flex flex-col h-screen justify-center items-center bg-yellow-200">
      
      <h1
        className="text-4xl animate-pulse"
      >Waiting for Item to be Scanned...</h1>
      <ScanListener/>
    </main>
  );
}
