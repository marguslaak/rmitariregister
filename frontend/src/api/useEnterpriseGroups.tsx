import { useQuery } from 'react-query';
import apiClient from './apiClient';
import { useMemo } from 'react';
import { EnterpriseGroup } from 'types/EnterpriseGroup';

const useEnterpriseGroups = () => {
  const { data, isFetching } = useQuery({
    queryKey: ['enterpriseGroups'],
    queryFn: async () => {
      const response = await apiClient.get<EnterpriseGroup[]>(
        `/raportid_enterprisegroups`
      );
      return response.data;
    },
  });

  const enterpriseGroups = useMemo(() => data || [], [data]);

  return { enterpriseGroups, isFetchingEnterpriseGroups: isFetching };
};

export default useEnterpriseGroups;
