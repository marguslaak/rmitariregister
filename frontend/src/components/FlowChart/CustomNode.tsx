import { Box, Text } from '@chakra-ui/react';
import { Handle, NodeProps, Position } from 'reactflow';

const CustomNode = ({ data }: NodeProps) => {
  return (
    <>
      <Handle type="target" position={Position.Top} />
      <Box>
        <Text>{data.label}</Text>
        {data.assets_value && (
          <Text color="green">
            {`(${new Intl.NumberFormat('et-EE', {
              style: 'currency',
              currency: 'EUR',
            }).format(data.assets_value)})`}
          </Text>
        )}
      </Box>
      <Handle type="source" position={Position.Bottom} id="a" />
      <Handle type="source" position={Position.Bottom} id="b" />
    </>
  );
};

export default CustomNode;
