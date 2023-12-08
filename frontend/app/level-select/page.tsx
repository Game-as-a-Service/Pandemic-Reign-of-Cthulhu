import { Button } from "@/components/ui/button";
import { levels } from "@/config/levels";

export default function LevelSelectDemo() {
  return (
    <main className="min-h-screen pb-48 bg-cover bg-map pt-11">
      <div className="container">
        <h1 className="text-6xl font-bold leading-tight text-center text-outline-4 xl:text-8xl text-yellow tracking-[4px]">
          Please Select the Level of Difficulty
          <span className="block leading-tight tracking-[20px]">
            請選擇難度
          </span>
        </h1>
        <div className="grid grid-rows-3 gap-16 pt-16 justify-items-center">
          {levels.map((level) => {
            return (
              <Button
                key={level.en}
                className="w-full h-auto transition-all bg-gradient-to-r from-tertiary to-secondary rounded-3xl py-14 shadow-custom hover:scale-95 active:scale-95"
                size="lg"
              >
                <span className="text-white font-bold tracking-[2px] text-outline-2 text-7xl xl:text-8xl">
                  {`${level.en} ${level.zh}`}
                </span>
              </Button>
            );
          })}
        </div>
      </div>
    </main>
  );
}
