type Investigator =
  | "detective"
  | "doctorate"
  | "driver"
  | "hunter"
  | "magician"
  | "occultist"
  | "reporter";
type Sanity = "sane" | "insane";

interface InvestigatorData {
  name: Investigator;
  saneImage: string;
  insaneImage: string;
  sanity: Sanity;
}
