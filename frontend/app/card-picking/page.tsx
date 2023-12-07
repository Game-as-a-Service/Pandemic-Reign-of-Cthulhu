import InvestigatorCard from "@/components/investigator-card2";
import { investigators } from "@/config/investigators";

export default function RolePickingDemo() {
  return (
    <main className="flex flex-col w-full h-full p-4 bg-cover gap-11 bg-map">
      <h1 className="font-bold leading-tight text-center text-outline text-7xl xl:text-8xl text-yellow">
        Please Select a Character
        <span className="block leading-tight tracking-[20px]">請選擇角色</span>
      </h1>
      <div className="grid grid-cols-4 gap-4 justify-items-center">
        {investigators.map((investigator) => {
          const { name, saneImage, sanity } = investigator;
          return (
            <InvestigatorCard
              key={name}
              investigator={name}
              imgUrl={saneImage}
              sanity={sanity}
            />
          );
        })}
      </div>
    </main>
  );
}
