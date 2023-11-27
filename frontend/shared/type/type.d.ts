type Investigator =
  | "detective"
  | "doctorate"
  | "driver"
  | "hunter"
  | "magician"
  | "occultist"
  | "reporter";
type Sanity = "sane" | "insane";
type City = 'Arkham' | 'Dunwich' | 'Kingsport' | 'Innsmouth';

interface InvestigatorData {
  name: Investigator;
  saneImage: string;
  insaneImage: string;
  sanity: Sanity;
}

