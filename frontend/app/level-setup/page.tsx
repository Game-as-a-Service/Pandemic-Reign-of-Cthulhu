import { Button } from "@/components/ui/button";
import { levels } from "@/config/levels";

export default function LevelSelectDemo() {
  return (
    <main className="min-h-full pb-48 bg-cover bg-map pt-11">
      <div className="container">
        <h1 className="text-5xl font-bold leading-tight text-center text-outline-4 xl:text-6xl 2xl:text-7xl text-yellow tracking-[4px]">
          Please Select the Level of Difficulty
          {/* <span className="block leading-tight tracking-[20px]">請選擇難度</span> */}
        </h1>
        <div className="grid grid-rows-3 gap-16 pt-16 justify-items-center">
          {levels.map((level) => {
            return (
              <Button key={level.label} variant="gradient" className="w-full h-36 xl:h-48 2xl:h-56">
                <span className="text-white font-bold tracking-[2px] text-outline-2 text-5xl xl:text-6xl 2xl:text-7xl">
                  {level.label}
                </span>
              </Button>
            );
          })}
        </div>
      </div>
    </main>
  );
}
