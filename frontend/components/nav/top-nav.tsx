"use client";
import { useMemo } from "react";
import Image from "next/image";
import { cn } from "@/lib/utils";

import { useAtom } from "jotai";
import {
  awakedOldOnes,
  cultistLeft,
  gateLeft,
  shoggothLeft,
} from "@/shared/atoms/game-status";
import { INVESTIGATOR_IMAGE_MAPPING } from "../investigator-card/constants";

export function TopNav() {
  const [oldOnesCount] = useAtom(awakedOldOnes);
  const [gateLeftCount] = useAtom(gateLeft);
  const [cultistLeftCount] = useAtom(cultistLeft);
  const [shoggothLeftCount] = useAtom(shoggothLeft);

  const user = {
    id: "demo-user",
    name: "Demo User",
    investigator: "driver",
    sane: true,
  };

  const profileImage = useMemo(() => {
    if (!user || !user.investigator || !user.sane) return;
    const sanity = user.sane ? "sane" : "insane";
    const investigator = user.investigator as Investigator;
    return INVESTIGATOR_IMAGE_MAPPING[`${investigator}-${sanity}`];
  }, [user]);

  return (
    <div className="flex flex-wrap w-full bg-green flex-row p-5 gap-3 rounded-b-2xl justify-between">
      <div className="flex gap-3 flex-row items-center">
        {profileImage && (
          <Image
            className={cn("rounded-full border-[3px] border-solid border-yellow", "border-yellow")}
            src={profileImage}
            alt={"profile"}
            width={50}
            height={50}
          />
        )}
        {user?.name && (
          <h2 className="lg:text-xl font-sans font-bold text-white">
            {user.name}
          </h2>
        )}
      </div>
      <div className="flex flex-row items-center justify-center gap-3">
        <h2 className="lg:text-xl font-sans font-bold text-white">
          Awaked Old Ones
        </h2>
        <h2 className="min-w-[30px] lg:text-xl font-sans font-bold text-white">
          x {oldOnesCount}
        </h2>
      </div>
      <div className="flex flex-row items-center justify-center gap-3">
        <h2 className="lg:text-xl font-sans font-bold text-white">
          Gates Left
        </h2>
        <h2 className="min-w-[30px] lg:text-xl font-sans font-bold text-white">
          x {gateLeftCount}
        </h2>
      </div>
      <div className="flex flex-row items-center justify-center gap-3">
        <h2 className="lg:text-xl font-sans font-bold text-white">
          Cultists Left
        </h2>
        <h2 className="min-w-[30px] lg:text-xl font-sans font-bold text-white">
          x {cultistLeftCount}
        </h2>
      </div>
      <div className="flex flex-row items-center justify-center gap-3">
        <h2 className="lg:text-xl font-sans font-bold text-white">
          Shoggoths Left
        </h2>
        <h2 className="min-w-[30px] lg:text-xl font-sans font-bold text-white">
          x {shoggothLeftCount}
        </h2>
      </div>
    </div>
  );
}
