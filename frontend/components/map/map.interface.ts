import { SimulationLinkDatum, SimulationNodeDatum } from "d3";

export interface MapNode extends SimulationNodeDatum {
    id: string
    city: City
    fx: number
    fy: number
    labelx: number
    labely: number
    isGate?: boolean
    isBusStation?: boolean
}

export interface MapLink extends SimulationLinkDatum<MapNode> {
    source: MapNode
    target: MapNode
}

export type MapData = {
    nodes: MapNode[]
    links: MapLink[]
}