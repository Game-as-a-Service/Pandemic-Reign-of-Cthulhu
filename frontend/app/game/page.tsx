import { GameMap } from "@/components/map";
import { Background } from "@/components/background";

export default function GamePage() {
  return (
    <>
      <Background cls=" h-full" isFullScreen={true}/>
      <section className="h-full flex flex-col justify-center items-center bg-brown/40">
       
        <div className="flex justify-center items-center p-4 w-full h-[80%]">
          <GameMap width={1080} height={720} />
        </div>
      </section>
    </>
  );
}
