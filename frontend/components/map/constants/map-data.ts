import { MapData } from "../map.interface";
import {
  BoardwalkNode,
  CafeNode,
  ChurchNode,
  DinerNode,
  DocksNode,
  FactoryNode,
  FarmsteadNode,
  GraveyardNode,
  GreatHallNode,
  HistoricInnNode,
  HospitalNode,
  JunkyardNode,
  MarketNode,
  OldMillNode,
  ParkNode,
  PawnShopNode,
  PoliceStationNode,
  SecretLodgeNode,
  SwampNode,
  TheaterNode,
  TrainStationNode,
  UniversityNode,
  WharfNode,
  WoodsNode,
} from "./nodes";

export const mapData: MapData = {
  nodes: [
    // Arkham Nodes
    TrainStationNode,
    UniversityNode,
    PoliceStationNode,
    DinerNode,
    SecretLodgeNode,
    ParkNode,

    // Dunwich Nodes
    CafeNode,
    OldMillNode,
    FarmsteadNode,
    ChurchNode,
    SwampNode,
    HistoricInnNode,

    // Kingsport Nodes
    GreatHallNode,
    TheaterNode,
    GraveyardNode,
    WharfNode,
    MarketNode,
    WoodsNode,

    // Innsmouth Nodes
    JunkyardNode,
    PawnShopNode,
    DocksNode,
    HospitalNode,
    FactoryNode,
    BoardwalkNode,
  ],
  links: [
    { source: TrainStationNode, target: UniversityNode },
    { source: UniversityNode, target: PoliceStationNode },
    { source: PoliceStationNode, target: ParkNode },
    { source: ParkNode, target: UniversityNode },

    { source: PoliceStationNode, target: SecretLodgeNode },
    { source: SecretLodgeNode, target: DinerNode },
    { source: ParkNode, target: SecretLodgeNode },
    { source: TrainStationNode, target: CafeNode },
    { source: DinerNode, target: JunkyardNode },

    { source: CafeNode, target: ChurchNode },
    { source: ChurchNode, target: OldMillNode },
    { source: ChurchNode, target: HistoricInnNode },
    { source: ChurchNode, target: FarmsteadNode },
    { source: HistoricInnNode, target: FarmsteadNode },
    { source: FarmsteadNode, target: SwampNode },
    { source: SwampNode, target: GreatHallNode },

    { source: JunkyardNode, target: PawnShopNode },
    { source: PawnShopNode, target: HospitalNode },
    { source: HospitalNode, target: FactoryNode },
    { source: FactoryNode, target: PawnShopNode },
    { source: FactoryNode, target: BoardwalkNode },
    { source: BoardwalkNode, target: DocksNode },
    { source: DocksNode, target: WoodsNode },

    { source: GreatHallNode, target: WoodsNode },
    { source: WoodsNode, target: MarketNode },
    { source: MarketNode, target: GreatHallNode },
    { source: MarketNode, target: TheaterNode },
    { source: MarketNode, target: WharfNode },
    { source: WharfNode, target: GraveyardNode },
  ],
};
