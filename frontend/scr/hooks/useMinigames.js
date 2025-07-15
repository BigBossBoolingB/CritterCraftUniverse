import { useState, useEffect, useCallback } from 'react';
import { notification } from 'antd';
import critterCraftAPI from '../crittercraft_api';

export const useMinigames = (pets = []) => {
  const [loading, setLoading] = useState(true);
  const [activeGames, setActiveGames] = useState([]);
  const [completedGames, setCompletedGames] = useState([]);
  const [actionLoading, setActionLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const fetchGames = useCallback(async () => {
    try {
      setRefreshing(true);
      const activeGameIds = await critterCraftAPI.getActiveGamesByPlayer();
      const activeGamesPromises = activeGameIds.map(id => critterCraftAPI.getGame(id));
      const activeGamesData = await Promise.all(activeGamesPromises);
      const completedGamesData = []; // Mock data
      setActiveGames(activeGamesData);
      setCompletedGames(completedGamesData);
    } catch (error) {
      console.error('Failed to fetch games:', error);
      notification.error({
        message: 'Failed to fetch games',
        description: error.message,
      });
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    fetchGames();
  }, [fetchGames]);

  const startGame = async (selectedPet, selectedGameType, selectedDifficulty) => {
    if (!selectedPet) {
      notification.warning({
        message: 'No pet selected',
        description: 'Please select a pet to play the game.',
      });
      return;
    }
    try {
      setActionLoading(true);
      const gameTypeIndex = gameTypes.findIndex(type => type.value === selectedGameType);
      const difficultyIndex = difficultyLevels.findIndex(level => level.value === selectedDifficulty);
      await critterCraftAPI.startGame(selectedPet, gameTypeIndex, difficultyIndex);
      notification.success({
        message: 'Game started',
        description: `You've started a ${selectedDifficulty} ${gameTypes.find(type => type.value === selectedGameType).label} game!`,
      });
      fetchGames();
    } catch (error) {
      console.error('Failed to start game:', error);
      notification.error({
        message: 'Failed to start game',
        description: error.message,
      });
    } finally {
      setActionLoading(false);
    }
  };

  const submitScore = async (selectedGameId, score) => {
    if (!selectedGameId) {
      notification.warning({
        message: 'No game selected',
        description: 'Please select a game to submit a score for.',
      });
      return;
    }
    try {
      setActionLoading(true);
      await critterCraftAPI.submitScore(selectedGameId, score);
      notification.success({
        message: 'Score submitted',
        description: `You've submitted a score of ${score} for your game!`,
      });
      fetchGames();
    } catch (error) {
      console.error('Failed to submit score:', error);
      notification.error({
        message: 'Failed to submit score',
        description: error.message,
      });
    } finally {
      setActionLoading(false);
    }
  };

  const cancelGame = async (gameId) => {
    try {
      setActionLoading(true);
      await critterCraftAPI.cancelGame(gameId);
      notification.success({
        message: 'Game canceled',
        description: 'The game has been canceled successfully.',
      });
      fetchGames();
    } catch (error) {
      console.error('Failed to cancel game:', error);
      notification.error({
        message: 'Failed to cancel game',
        description: error.message,
      });
    } finally {
      setActionLoading(false);
    }
  };

  return {
    loading,
    activeGames,
    completedGames,
    actionLoading,
    refreshing,
    fetchGames,
    startGame,
    submitScore,
    cancelGame,
  };
};

export const gameTypes = [
  { value: 'LogicLeaper', label: 'Logic Leaper', description: 'A puzzle game that trains Intelligence' },
  { value: 'AuraWeaving', label: 'Aura Weaving', description: 'A rhythm game that trains Charisma' },
  { value: 'HabitatDash', label: 'Habitat Dash', description: 'An endless runner that trains Agility' },
];

export const difficultyLevels = [
  { value: 'Easy', label: 'Easy', multiplier: '1x' },
  { value: 'Medium', label: 'Medium', multiplier: '2x' },
  { value: 'Hard', label: 'Hard', multiplier: '3x' },
  { value: 'Expert', label: 'Expert', multiplier: '4x' },
];
