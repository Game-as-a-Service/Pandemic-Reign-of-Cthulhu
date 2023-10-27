import {
  DetectiveSane,
  DoctorateSane,
  DriverSane,
  HunterSane,
  MagicianSane,
  OccultistSane,
  ReporterSane,
  SaneSign,
  SaneStrokeText,
} from "@/assets/investigator/sane";
import {
  DetectiveInsane,
  DoctorateInsane,
  DriverInsane,
  HunterInsane,
  InsaneSign,
  InsantStrokeText,
  MagicianInsane,
  OccultistInsane,
  ReporterInsane,
} from "@/assets/investigator/insane";

export const SANITY_STROKE_TEXT_MAPPING = {
  "sane": SaneStrokeText,
  "insane": InsantStrokeText
}

export const SANITY_SIGN_MAPPING = {
  "sane": SaneSign,
  "insane": InsaneSign
}

export const INVESTIGATOR_IMAGE_MAPPING = {
  "detective-sane": DetectiveSane,
  "doctorate-sane": DoctorateSane,
  "driver-sane": DriverSane,
  "hunter-sane": HunterSane,
  "magician-sane": MagicianSane,
  "occultist-sane": OccultistSane,
  "reporter-sane": ReporterSane,
  'sign-sane': SaneSign,
  "detective-insane": DetectiveInsane,
  "doctorate-insane": DoctorateInsane,
  "driver-insane": DriverInsane,
  "hunter-insane": HunterInsane,
  "magician-insane": MagicianInsane,
  "occultist-insane": OccultistInsane,
  "reporter-insane": ReporterInsane,
  'insane-sign': InsaneSign
};
