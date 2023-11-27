"use client";
import * as d3 from "d3";
import { useEffect, useRef } from "react";
import { RADIUS, drawMap } from "./draw-map";
import { MapLink, MapNode } from "./map.interface";
import { mapData } from "./constants";

type NetworkDiagramProps = {
  width: number;
  height: number;
};

export const GameMap = ({
  width,
  height,
}: NetworkDiagramProps) => {
  // The force simulation mutates links and nodes, so create a copy first
  // Node positions are initialized by d3
  const links: MapLink[] = mapData.links.map((d) => ({ ...d }));
  const nodes: MapNode[] = mapData.nodes.map((d) => ({ ...d }));

  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    // set dimension of the canvas element
    const canvas = canvasRef.current;
    const context = canvas?.getContext("2d");

    if (!context) {
      return;
    }

    // run d3-force to find the position of nodes on the canvas
    d3.forceSimulation(nodes)
      .force(
        "link",
        d3.forceLink<MapNode, MapLink>(links).id((d) => d.id)
      )
      .force("collide", d3.forceCollide().radius(RADIUS))
      .force("charge", d3.forceManyBody().strength(-30))
      .force("center", d3.forceCenter(width / 2, height / 2))

      // at each iteration of the simulation, draw the network diagram with the new node positions
      .on("tick", () => {
        drawMap(context, width, height, nodes, links);
      });
  }, [width, height, nodes, links]);

  return (
    <canvas
      className="max-w-full max-h-[720px]"
      ref={canvasRef}
      width={width}
      height={height}
    />
  );
};
