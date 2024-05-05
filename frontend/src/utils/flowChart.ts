import Dagre from '@dagrejs/dagre';
import { Node, Edge, MarkerType } from 'reactflow';

const dagreGraph = new Dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));

export const getLayoutedElements = (
  nodes: Node[],
  edges: Edge[],
  direction: string
) => {
  dagreGraph.setGraph({ rankdir: direction, nodesep: 100, edgesep: 10 });

  edges.forEach((edge: Edge) => dagreGraph.setEdge(edge.source, edge.target));
  nodes.forEach((node: Node) => dagreGraph.setNode(node.id, node as any));

  Dagre.layout(dagreGraph);

  return {
    nodes: nodes.map((node: Node) => {
      const { x, y } = dagreGraph.node(node.id);

      return { ...node, position: { x, y } };
    }),
    edges,
  };
};

export const edgeCommons = {
  animated: true,
  markerEnd: {
    type: MarkerType.ArrowClosed,
    width: 16,
    height: 16,
    color: '#FF0072',
  },
  style: {
    strokeWidth: 2,
    stroke: '#FF0072',
  },
  type: 'highlightable',
};
