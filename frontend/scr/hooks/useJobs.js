import { useState, useEffect, useCallback } from 'react';
import { notification, Button } from 'antd';
import critterCraftAPI, { ConnectionError, TransactionError, QueryError, WalletError } from '../crittercraft_api_improved';

export const useJobs = (pets = []) => {
  const [loading, setLoading] = useState(true);
  const [activeJobs, setActiveJobs] = useState([]);
  const [completedJobs, setCompletedJobs] = useState([]);
  const [actionLoading, setActionLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState({
    connected: critterCraftAPI.isConnected,
    checking: false,
  });
  const [walletStatus, setWalletStatus] = useState({
    connected: false,
    accounts: [],
    loading: false,
  });

  const handleError = (error, context) => {
    console.error(`Error in ${context}:`, error);
    if (error instanceof ConnectionError) {
      notification.error({
        message: 'Connection Error',
        description: `Failed to connect to the blockchain: ${error.message}`,
        duration: 0,
      });
    } else if (error instanceof WalletError) {
      notification.error({
        message: 'Wallet Error',
        description: error.message,
      });
    } else if (error instanceof TransactionError) {
      notification.error({
        message: 'Transaction Failed',
        description: error.message,
      });
    } else if (error instanceof QueryError) {
      notification.error({
        message: 'Data Fetch Error',
        description: `Failed to fetch data: ${error.message}`,
      });
    } else {
      notification.error({
        message: `Error in ${context}`,
        description: error.message || 'An unknown error occurred',
      });
    }
  };

  const fetchJobs = useCallback(async () => {
    try {
      setRefreshing(true);
      const activeJobIds = await critterCraftAPI.getActiveJobsByOwner();
      const activeJobsPromises = activeJobIds.map(id => critterCraftAPI.getJob(id));
      const activeJobsData = await Promise.all(activeJobsPromises);
      const completedJobsData = await critterCraftAPI.getCompletedJobsByOwner(null, 10);
      setActiveJobs(activeJobsData);
      setCompletedJobs(completedJobsData);
    } catch (error) {
      handleError(error, 'fetching jobs');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  const connectWallet = useCallback(async () => {
    try {
      setWalletStatus(prev => ({ ...prev, loading: true }));
      const accounts = await critterCraftAPI.connectWallet();
      if (accounts.length > 0) {
        critterCraftAPI.setAccount(accounts[0]);
      }
      setWalletStatus({
        connected: accounts.length > 0,
        accounts: accounts,
        loading: false,
      });
      notification.success({
        message: 'Wallet Connected',
        description: `Connected to wallet with ${accounts.length} accounts.`,
      });
      fetchJobs();
    } catch (error) {
      setWalletStatus({
        connected: false,
        accounts: [],
        loading: false,
      });
      handleError(error, 'wallet connection');
    }
  }, [fetchJobs]);

  const checkConnection = useCallback(async () => {
    setConnectionStatus(prev => ({ ...prev, checking: true }));
    try {
      const connected = await critterCraftAPI.connect();
      setConnectionStatus({ connected, checking: false });
      if (connected) {
        fetchJobs();
      }
    } catch (error) {
      setConnectionStatus({ connected: false, checking: false });
      notification.error({
        message: 'Connection Failed',
        description: error.message,
      });
    }
  }, [fetchJobs]);

  useEffect(() => {
    checkConnection();
  }, [checkConnection]);

  const startJob = async (selectedPet, selectedJobType, duration) => {
    if (!selectedPet) {
      notification.warning({
        message: 'No pet selected',
        description: 'Please select a pet for the job.',
      });
      return;
    }
    try {
      setActionLoading(true);
      const jobTypeIndex = jobTypes.findIndex(type => type.value === selectedJobType);
      const selectedJobTypeInfo = jobTypes.find(type => type.value === selectedJobType);
      await critterCraftAPI.startJob(selectedPet, jobTypeIndex, duration);
      notification.success({
        message: 'Job Started',
        description: `Your pet has started a ${selectedJobTypeInfo.label} job!`,
      });
      fetchJobs();
    } catch (error) {
      handleError(error, 'starting job');
      if (error instanceof ConnectionError) {
        notification.info({
          message: 'Reconnection Available',
          description: 'You can try to reconnect to the blockchain.',
          btn: <Button type="primary" onClick={checkConnection}>Reconnect</Button>,
          duration: 10,
        });
      }
    } finally {
      setActionLoading(false);
    }
  };

  const completeJob = async (jobId) => {
    try {
      setActionLoading(true);
      await critterCraftAPI.completeJob(jobId);
      notification.success({
        message: 'Job Completed',
        description: 'The job has been completed successfully!',
        icon: <CheckCircleOutlined style={{ color: '#52c41a' }} />,
      });
      fetchJobs();
    } catch (error) {
      handleError(error, 'completing job');
      if (error instanceof ConnectionError) {
        notification.info({
          message: 'Reconnection Available',
          description: 'You can try to reconnect to the blockchain.',
          btn: <Button type="primary" onClick={checkConnection}>Reconnect</Button>,
          duration: 10,
        });
      }
    } finally {
      setActionLoading(false);
    }
  };

  const cancelJob = async (jobId) => {
    try {
      setActionLoading(true);
      await critterCraftAPI.cancelJob(jobId);
      notification.success({
        message: 'Job Canceled',
        description: 'The job has been canceled successfully.',
        icon: <CloseCircleOutlined style={{ color: '#ff4d4f' }} />,
      });
      fetchJobs();
    } catch (error) {
      handleError(error, 'canceling job');
      if (error instanceof ConnectionError) {
        notification.info({
          message: 'Reconnection Available',
          description: 'You can try to reconnect to the blockchain.',
          btn: <Button type="primary" onClick={checkConnection}>Reconnect</Button>,
          duration: 10,
        });
      }
    } finally {
      setActionLoading(false);
    }
  };

  return {
    loading,
    activeJobs,
    completedJobs,
    actionLoading,
    refreshing,
    connectionStatus,
    walletStatus,
    fetchJobs,
    connectWallet,
    checkConnection,
    startJob,
    completeJob,
    cancelJob,
  };
};

export const jobTypes = [
  { value: 'CrystalMining', label: 'Crystal Mining', stat: 'Strength', description: 'Mine crystals in the caves' },
  { value: 'BioluminescentGuide', label: 'Bioluminescent Guide', stat: 'Charisma', description: 'Guide visitors through bioluminescent areas' },
  { value: 'HerbalistAssistant', label: 'Herbalist Assistant', stat: 'Intelligence', description: 'Assist the herbalist in gathering and processing herbs' },
];
