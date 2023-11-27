import { CityColorMapping } from "./constants";
import { MapLink, MapNode } from "./map.interface";

export const RADIUS = 22.5;

export const drawMap = (
  context: CanvasRenderingContext2D,
  width: number,
  height: number,
  nodes: MapNode[],
  links: MapLink[]
) => {
  context.clearRect(0, 0, width, height);

  // Draw the links first
  links.forEach((link) => {
    context.beginPath();
    context.moveTo(link.source.fx, link.source.fy);
    context.lineTo(link.target.fx, link.target.fy);
    context.strokeStyle = '#fff'
    context.stroke();
  });

  // Draw the nodes
  nodes.forEach((node) => {
    if (!node.fx || !node.fy) return;
    if(node.isGate) {
      const gate = new Image()
      gate.src = './props/gate.png'
      gate.onload = () => { context.drawImage(gate, node.fx - RADIUS, node.fy - RADIUS, RADIUS * 2, RADIUS * 2)}
    }

    if(node.isBusStation) {
      const labelWidth = context.measureText(node.id).width
      const bus = new Image()
      bus.src = './props/bus.png'
      bus.onload = () => { context.drawImage(bus, node.labelx + labelWidth / 2 - 12.5, node.labely, 25, 25)}
    }

    /* draw node */
    context.beginPath();
    context.moveTo(node.fx + RADIUS, node.fy);
    context.arc(node.fx, node.fy, RADIUS, 0, 2 * Math.PI);
    context.closePath()
    
    /* node styling */
    const gradient = context.createLinearGradient(node.fx - RADIUS, node.fy - RADIUS, node.fx + RADIUS, node.fy + RADIUS)
    const cityColor = CityColorMapping[node.city]
    gradient.addColorStop(0, cityColor.startColor)
    gradient.addColorStop(1, cityColor.endColor)
    context.fillStyle = gradient

    context.shadowColor = "#333";
    context.shadowOffsetX = 4;
    context.shadowOffsetY = 4
    context.shadowBlur = 16;

    context.strokeStyle = '#fff'
    context.lineWidth = 2
    context.fill();
    context.stroke();

    /* node label */
    context.beginPath();
    context.font = 'bold 16px Noto Sans'
    context.fillStyle = '#fff'
    context.fillText(node.id, node.labelx, node.isBusStation ? node.labely - 7.5 : node.labely)
  });
};
