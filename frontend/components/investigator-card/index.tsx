"use client";
import { useMemo } from "react";
import { INVESTIGATOR_IMAGE_MAPPING, SANITY_SIGN_MAPPING, SANITY_STROKE_TEXT_MAPPING } from "./constants";
import Image from "next/image";
import { cn } from "@/lib/utils";

interface Props {
  investigator: Investigator;
  sane: boolean;
}

export const InvestigatorCard = ({ investigator, sane }: Props) => {
  const sanity = sane ? "sane" : "insane";
  const image = useMemo(() => {
    return INVESTIGATOR_IMAGE_MAPPING[`${investigator}-${sanity}`];
  }, [investigator, sane]);

  const sanitySign = useMemo(() => { return SANITY_SIGN_MAPPING[sanity] }, [sanity]);

  const sanityText = useMemo(() => { return SANITY_STROKE_TEXT_MAPPING[sanity] }, [sanity]);

  return (
    <div
      className={cn(
        "rounded-2xl w-60 min-h-[250px] bg-gradient-to-r shadow-lg",
        sane ? "from-tertiary to-brown" : "from-primary to-secondary"
      )}
    >
      <div className="absolute ml-3 mt-3">
       <Image src={sanityText} alt="sanity" width={50} height={75} className="h-6 w-auto" />
      </div>
      <div className="w-full h-auto">
        <Image
          src={image}
          alt={`investigator-card`}
          width={250}
          height={250}
          className="rounded-t-2xl"
        />
      </div>
      <div className="flex w-full gap-3 justify-center align-center relative py-2 px-4 min-h-[45px]">
        <h1 className="text-white capitalize text-2xl font-display">
          {investigator}
        </h1>
        <div className="absolute right-1 bottom-1">
          <Image src={sanitySign} alt={`sanity-sign`} width={35} height={35} />
        </div>
      </div>

    </div>
  );
};
