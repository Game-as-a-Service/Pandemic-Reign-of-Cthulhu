"use client";
import React, { useMemo, useState } from "react";
import Image from "next/image";
import { cn } from "@/lib/utils";
import { Card, CardFooter, CardHeader, CardTitle } from "../ui/card";

interface InvestigatorCardProps {
  investigator: Investigator;
  imgUrl: string;
  sanity: Sanity;
}

const InvestigatorCard = React.memo(function ({
  investigator,
  imgUrl,
  sanity,
}: InvestigatorCardProps) {
  const [isSelected, setIsSelected] = useState(false);

  const gradientStyle = useMemo(
    () => ({
      sane: "from-tertiary to-brown",
      insane: "from-primary to-secondary",
    }),
    []
  );

  const sanityText = useMemo(
    () => ({
      sane: "/img/sane-stroke-text.svg",
      insane: "/img/insane-stroke-text.svg",
    }),
    []
  );

  const sanitySign = useMemo(
    () => ({
      sane: "/img/sane-sign.png",
      insane: "/img/insane-sign.png",
    }),
    []
  );

  return (
    <Card
      className={cn(
        "rounded-2xl w-60 min-h-[250px] border-0 bg-gradient-to-r shadow-lg cursor-pointer transition-all",
        "hover:scale-99 active:scale-99 group",
        gradientStyle[sanity],
        isSelected ? "grayscale" : "grayscale-0"
      )}
      onClick={() => setIsSelected((v) => !v)}
    >
      <CardHeader className="relative w-full h-auto p-0">
        <Image
          src={imgUrl}
          alt={`investigator-card`}
          width={250}
          height={250}
          priority
          className="rounded-t-2xl group-hover:opacity-80 group-active:opacity-80"
        />
        <div className="absolute top-3 left-3">
          <Image
            src={sanityText[sanity]}
            alt="sanity"
            width={50}
            height={75}
            className="w-auto h-6"
          />
        </div>
      </CardHeader>
      <CardFooter className="w-full gap-3 justify-center align-center relative py-2 px-4 min-h-[45px]">
        <CardTitle className="text-2xl tracking-wider text-white capitalize font-display">
          {investigator}
        </CardTitle>
        <div className="absolute right-1 bottom-1">
          <Image src={sanitySign[sanity]} alt={`sanity-sign`} width={35} height={35} />
        </div>
      </CardFooter>
    </Card>
  );
});

InvestigatorCard.displayName = "InvestigatorCard";
export default InvestigatorCard;
