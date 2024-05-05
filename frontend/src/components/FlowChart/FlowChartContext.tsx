import {
  createContext,
  useContext,
  type Dispatch,
  type ReactNode,
  type SetStateAction,
  useState,
} from 'react';
import { Node } from 'reactflow';

interface ContextState {
  selectedNode: Node | undefined;
  setSelectedNode: Dispatch<SetStateAction<Node | undefined>>;
}

export const FlowChartContext = createContext<ContextState>({} as ContextState);

const FlowChartContextProvider = ({ children }: { children: ReactNode }) => {
  const [selectedNode, setSelectedNode] = useState<Node>();

  const value: ContextState = {
    selectedNode,
    setSelectedNode,
  };

  return (
    <FlowChartContext.Provider value={value}>
      {children}
    </FlowChartContext.Provider>
  );
};

export const useFlowChartContext = () => {
  return useContext(FlowChartContext);
};

export default FlowChartContextProvider;
