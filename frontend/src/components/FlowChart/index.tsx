import { useCallback, useMemo, useState } from 'react';
import { useDebounce, useWindowSize } from 'react-use';
import ReactFlow, {
  ReactFlowProvider,
  Panel,
  useNodesState,
  useEdgesState,
  useReactFlow,
  Background,
  Controls,
  MiniMap,
  Edge,
  Node,
} from 'reactflow';

import { getLayoutedElements } from 'utils/flowChart';
import FlowChartContextProvider, {
  useFlowChartContext,
} from './FlowChartContext';

import { Heading, Radio, RadioGroup, Stack, useToken } from '@chakra-ui/react';

import CustomNode from './CustomNode';
import CustomEdge from './CustomEdge';

import 'reactflow/dist/style.css';

type Props = {
  focusId: number;
  initialNodes: {
    id: string;
    data: {
      label: string;
    };
    position: {
      x: number;
      y: number;
    };
  }[];
  initialEdges: Edge[];
};
const LayoutFlow = ({ focusId, initialNodes, initialEdges }: Props) => {
  const { fitView } = useReactFlow();
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [layout, setLayout] = useState<string>();
  const { setSelectedNode } = useFlowChartContext();
  const { width, height } = useWindowSize();
  const [gray100] = useToken('colors', ['gray.100']);

  const createLayout = useCallback(
    (newNodes: Node[], newEdges: Edge[], direction: string) => {
      const layouted = getLayoutedElements(
        [...newNodes],
        [...newEdges],
        direction
      );

      setNodes([...layouted.nodes]);
      setEdges([...layouted.edges]);

      setLayout(direction);

      setTimeout(() => {
        window.requestAnimationFrame(() => {
          fitView();
        });
      }, 100);
    },
    [fitView, setEdges, setNodes]
  );

  useDebounce(
    () => {
      createLayout(nodes, edges, layout || 'LR');
    },
    300,
    [width, height]
  );

  useDebounce(
    () => {
      createLayout(initialNodes, initialEdges, layout || 'LR');
    },
    300,
    [initialEdges, initialNodes]
  );

  const edgeTypes = useMemo(
    () => ({
      highlightable: CustomEdge,
    }),
    []
  );
  const nodeTypes = useMemo(
    () => ({
      default: CustomNode,
    }),
    []
  );

  return (
    <ReactFlow
      key={focusId}
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onSelectionChange={({ nodes }) => {
        if (nodes.length > 0) setSelectedNode(nodes[0]);
      }}
      nodeTypes={nodeTypes}
      edgeTypes={edgeTypes}
      fitView
    >
      <Panel
        position="top-left"
        style={{ backgroundColor: gray100, padding: '16px', left: 0 }}
      >
        <Heading size="sm" mb={2}>
          Paigutus
        </Heading>
        <RadioGroup
          onChange={(val: string) => createLayout(nodes, edges, val)}
          value={layout}
        >
          <Stack direction="row">
            <Radio value="TB">Horisontaalne</Radio>
            <Radio value="LR">Vertikaalne</Radio>
          </Stack>
        </RadioGroup>
      </Panel>
      <Background />
      <Controls />
      <MiniMap nodeStrokeWidth={3} />
    </ReactFlow>
  );
};

const FlowChart = (props: Props) => (
  <ReactFlowProvider>
    <FlowChartContextProvider>
      <LayoutFlow {...props} />
    </FlowChartContextProvider>
  </ReactFlowProvider>
);

export default FlowChart;
