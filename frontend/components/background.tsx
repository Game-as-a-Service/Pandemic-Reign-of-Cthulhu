import bgImage from "@/assets/background.png";
import { cn } from "@/lib/utils";
import Image from "next/image";

interface Props {
    isFullScreen?: boolean
    cls?: string
}
export const Background = ({ isFullScreen = false, cls }: Props) => {
  return (
    <div className={cn("w-full h-full", isFullScreen &&  "absolute z-[-10]", cls)}>
      <Image
        src={bgImage}
        fill
        alt="map-background"
        className={cn('object-center', isFullScreen ? 'object-cover' : 'object-contain')}
      />
    </div>
  );
};
