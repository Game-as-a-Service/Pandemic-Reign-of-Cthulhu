import { InvestigatorCard } from "@/components/investigator-card";
import { INVESTIGATORS } from "@/shared/constants";

export default function DesignSystem() {
  return (
    <section className="flex w-full h-full overflow-y-scroll flex-col gap-4 p-4">
      <h1 className="text-primary text-3xl font-bold">Design System</h1>
      <div className="flex flex-col gap-4 w-full">
        <h2>Investigator Card</h2>
        <div className="grid grid-cols-4 gap-4">
          {INVESTIGATORS.map((investigator: string) => {
            // showcase all the investigator cards
            const sanity = [true, false];
            return sanity.map((sane: boolean) => {
              return (
                <InvestigatorCard
                  key={`${investigator}-${String(sane)}`}
                  investigator={investigator as Investigator}
                  sane={sane}
                />
              );
            });
          })}
        </div>
      </div>
    </section>
  );
}
