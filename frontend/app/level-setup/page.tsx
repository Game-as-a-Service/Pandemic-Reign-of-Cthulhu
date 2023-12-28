import { Button } from "@/components/ui/button";
import { levels } from "@/config/levels";

export default function LevelSelectDemo() {
  return (
    <main className="min-h-full py-8 bg-cover bg-map">
      <div className="container">
        <h1 className="text-5xl font-bold leading-tight text-center text-outline-4 xl:text-6xl 2xl:text-7xl text-yellow tracking-[4px]">
          Please Select the Level of Difficulty
          {/* <span className="block leading-tight tracking-[20px]">請選擇難度</span> */}
        </h1>
        <div className="grid grid-rows-3 grid-cols-1 gap-6 xl:gap-10 2xl:gap-12 mt-11 justify-items-center">
          {levels.map((level) => {
            return (
              <div className="w-full lg:px-10 xl:px-20 2xl:px-32" key={level.label}>
                <Button variant="gradient" className="w-full h-28 xl:h-36 2xl:h-44">
                  <span className="text-white font-bold tracking-[2px] text-outline-2 text-4xl xl:text-5xl 2xl:text-6xl">
                    {level.label}
                  </span>
                </Button>
              </div>
            );
          })}
        </div>
      </div>
    </main>
  );
}
