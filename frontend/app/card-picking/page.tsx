import InvestigatorCard from "@/components/investigator-card2";
import { investigators } from "@/config/investigators";

export default function RolePickingDemo() {
  return (
    <main className="min-h-full py-4 bg-cover bg-map">
      <div className="container">
        <h1 className="font-bold leading-tight text-center text-outline-4 tracking-[4px] text-7xl xl:text-8xl text-yellow">
          Please Select a Character
          {/* <span className="block leading-tight tracking-[20px]">請選擇角色</span> */}
        </h1>
        <div className="flex flex-wrap items-center justify-center gap-4 xl:gap-8 2xl:gap-10 mt-11">
          {investigators.map((investigator) => {
            const { name, saneImage, sanity } = investigator;
            return (
              <InvestigatorCard key={name} investigator={name} imgUrl={saneImage} sanity={sanity} />
            );
          })}
        </div>
      </div>
    </main>
  );
}
