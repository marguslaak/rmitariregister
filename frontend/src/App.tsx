import { useEffect, useMemo, useState } from 'react';

import useEnterprises from 'api/useEnterprises';
import useEnterpriseGroups from 'api/useEnterpriseGroups';
import { EnterpriseGroup } from 'types/EnterpriseGroup';
import { edgeCommons } from 'utils/flowChart';
import { useDebounce } from 'utils/hooks/useDebounce';

import {
  Box,
  Container,
  Flex,
  Grid,
  Input,
  Link,
  ListItem,
  SkeletonText,
  Stack,
  Text,
  UnorderedList,
} from '@chakra-ui/react';

import FlowChart from 'components/FlowChart';

import 'react-toastify/dist/ReactToastify.css';

const App = () => {
  const [search, setSearch] = useState<string>('');
  const debouncedSearch = useDebounce(search, 400);

  const [selectedEnterpriseId, setSelectedEnterpriseId] = useState<number>();
  const [searchResults, setSearchResults] = useState<EnterpriseGroup[]>([]);

  const { enterprises, isFetchingEnterprises } = useEnterprises();
  const { enterpriseGroups, isFetchingEnterpriseGroups } =
    useEnterpriseGroups();

  useEffect(() => {
    if (debouncedSearch.length >= 3) {
      setSearchResults(
        enterpriseGroups.filter(({ name }) =>
          name.toLowerCase().includes(debouncedSearch.toLowerCase())
        )
      );
    } else {
      if (enterpriseGroups.length > 0) setSearchResults(enterpriseGroups);
    }
  }, [enterpriseGroups, debouncedSearch]);

  const nodes = useMemo(() => {
    if (selectedEnterpriseId) {
      const mainEnterprise = enterpriseGroups.find(
        ({ id }) => id === selectedEnterpriseId
      );
      const relatedEnterprises = enterprises.filter(
        ({ group_id }) => group_id === selectedEnterpriseId
      );

      if (mainEnterprise) {
        return [
          {
            id: String(mainEnterprise.enterprise_id),
            data: {
              label: mainEnterprise.name,
              assets_value: mainEnterprise.assets_value,
            },
            position: { x: 0, y: 0 },
          },
          ...relatedEnterprises.map(row => ({
            id: String(row.id),
            data: { label: row.name, assets_value: row.assets_value },
            position: { x: 0, y: 0 },
          })),
        ];
      } else return [];
    } else return [];
  }, [selectedEnterpriseId, enterprises, enterpriseGroups]);

  const edges = useMemo(() => {
    if (selectedEnterpriseId) {
      const relatedEnterprises = enterprises.filter(
        ({ group_id }) => group_id === selectedEnterpriseId
      );
      return relatedEnterprises.map(row => ({
        id: `e${row.id}-${row.owner_id}-${Math.random() * 1000}`,
        source: String(row.id),
        target: row.owner_id
          ? String(row.owner_id)
          : String(selectedEnterpriseId),
        label: row.share_percentage ? `${row.share_percentage}%` : '',
        ...edgeCommons,
      }));
    } else return [];
  }, [enterprises, selectedEnterpriseId]);

  const isLoadingData = isFetchingEnterprises || isFetchingEnterpriseGroups;

  return (
    <Container maxW="9xl" py={10}>
      <Grid
        gridTemplateColumns={{
          base: '1fr',
          md: '1fr 3fr',
        }}
        gridTemplateRows={'auto'}
        gridTemplateAreas={{
          base: `'list' 'charts'`,
          md: `'list charts'`,
        }}
      >
        <Box gridArea="list" bg="gray.100" px={4} py={6}>
          <Stack gap={6}>
            <Input
              placeholder="Otsi emaettevõtet, min 3 tähte"
              bg="white"
              onChange={e => setSearch(e.target.value)}
              isDisabled={isLoadingData}
            />
            <UnorderedList
              listStyleType="none"
              ml={0}
              maxH="80vh"
              overflowY="auto"
            >
              {isLoadingData && (
                <SkeletonText
                  mt="4"
                  noOfLines={20}
                  spacing="4"
                  skeletonHeight="2"
                  cursor="wait"
                />
              )}
              {!isLoadingData && (
                <>
                  {searchResults
                    .sort(
                      (a, b) => (b?.assets_value ?? 0) - (a.assets_value ?? 0)
                    )
                    .map(({ id, name, assets_value }) => (
                      <ListItem
                        key={`enterprise-${id}`}
                        p={3}
                        backgroundColor={
                          selectedEnterpriseId === id
                            ? 'gray.300'
                            : 'transparent'
                        }
                        _hover={{ backgroundColor: 'gray.300' }}
                      >
                        <Link onClick={() => setSelectedEnterpriseId(id)}>
                          {name}{' '}
                          <Text color="green">
                            {assets_value
                              ? `(${new Intl.NumberFormat('et-EE', {
                                  style: 'currency',
                                  currency: 'EUR',
                                }).format(assets_value)})`
                              : ''}
                          </Text>
                        </Link>
                      </ListItem>
                    ))}
                </>
              )}
            </UnorderedList>
          </Stack>
        </Box>
        <Box gridArea="charts" p={2}>
          <Flex gap={6} flexDirection="column" w="full" height={'80vh'}>
            {!!selectedEnterpriseId && (
              <FlowChart
                focusId={selectedEnterpriseId}
                initialNodes={nodes}
                initialEdges={edges}
              />
            )}
          </Flex>
        </Box>
      </Grid>
    </Container>
  );
};

export default App;
