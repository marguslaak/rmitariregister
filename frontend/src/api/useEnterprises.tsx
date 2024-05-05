import { useQuery } from 'react-query';
import apiClient from './apiClient';
import { useMemo } from 'react';
import { Enterprise } from 'types/Enterprise';

const useEnterprises = () => {
  const { data, isFetching } = useQuery({
    queryKey: ['enterprises'],
    queryFn: async () => {
      const response = await apiClient.get<Enterprise[]>(
        `/raportid_enterprises`
      );
      return response.data;
    },
  });

  const enterprises = useMemo(() => data || [], [data]);

  return { enterprises, isFetchingEnterprises: isFetching };
};

export default useEnterprises;
