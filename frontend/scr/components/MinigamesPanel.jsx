import React, { useState } from 'react';
import { Card, Button, Select, Table, Tag, Modal, InputNumber, Spin, notification, Tabs, Statistic, Row, Col } from 'antd';
import {
  TrophyOutlined,
  RocketOutlined,
  BulbOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  PlayCircleOutlined,
} from '@ant-design/icons';
import { useMinigames, gameTypes, difficultyLevels } from '../hooks/useMinigames';

const { Option } = Select;
const { TabPane } = Tabs;

/**
 * MinigamesPanel component for starting and managing mini-games
 */
const MinigamesPanel = ({ pets = [] }) => {
  const {
    loading,
    activeGames,
    completedGames,
    actionLoading,
    refreshing,
    fetchGames,
    startGame,
    submitScore,
    cancelGame,
  } = useMinigames(pets);

  const [startGameModalVisible, setStartGameModalVisible] = useState(false);
  const [submitScoreModalVisible, setSubmitScoreModalVisible] = useState(false);
  const [selectedPet, setSelectedPet] = useState(null);
  const [selectedGameType, setSelectedGameType] = useState('LogicLeaper');
  const [selectedDifficulty, setSelectedDifficulty] = useState('Easy');
  const [selectedGameId, setSelectedGameId] = useState(null);
  const [score, setScore] = useState(1000);

  const handleStartGame = () => {
    startGame(selectedPet, selectedGameType, selectedDifficulty);
    setStartGameModalVisible(false);
  };

  const handleSubmitScore = () => {
    submitScore(selectedGameId, score);
    setSubmitScoreModalVisible(false);
  };

  const handleCancelGame = (gameId) => {
    cancelGame(gameId);
  };

  // Open the submit score modal
  const openSubmitScoreModal = (gameId) => {
    setSelectedGameId(gameId);
    setSubmitScoreModalVisible(true);
  };

  // Columns for the active games table
  const activeGamesColumns = [
    {
      title: 'Game',
      dataIndex: 'game_type',
      key: 'game_type',
      render: (gameType) => {
        const game = gameTypes.find(type => type.value === gameType);
        return game ? game.label : gameType;
      },
    },
    {
      title: 'Pet',
      dataIndex: 'pet_id',
      key: 'pet_id',
      render: (petId) => {
        const pet = pets.find(p => p.id === petId);
        return pet ? pet.name : `Pet #${petId}`;
      },
    },
    {
      title: 'Difficulty',
      dataIndex: 'difficulty',
      key: 'difficulty',
      render: (difficulty) => {
        const level = difficultyLevels.find(level => level.value === difficulty);
        return level ? (
          <Tag color={
            difficulty === 'Easy' ? 'green' :
            difficulty === 'Medium' ? 'blue' :
            difficulty === 'Hard' ? 'orange' :
            'red'
          }>
            {level.label}
          </Tag>
        ) : difficulty;
      },
    },
    {
      title: 'Started',
      dataIndex: 'started_at',
      key: 'started_at',
      render: (startedAt) => new Date(startedAt).toLocaleString(),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <div>
          <Button 
            type="primary" 
            icon={<CheckCircleOutlined />} 
            onClick={() => openSubmitScoreModal(record.id)}
            style={{ marginRight: 8 }}
          >
            Submit Score
          </Button>
          <Button 
            danger 
            icon={<CloseCircleOutlined />} 
            onClick={() => handleCancelGame(record.id)}
          >
            Cancel
          </Button>
        </div>
      ),
    },
  ];

  // Columns for the completed games table
  const completedGamesColumns = [
    {
      title: 'Game',
      dataIndex: 'game_type',
      key: 'game_type',
      render: (gameType) => {
        const game = gameTypes.find(type => type.value === gameType);
        return game ? game.label : gameType;
      },
    },
    {
      title: 'Pet',
      dataIndex: 'pet_id',
      key: 'pet_id',
      render: (petId) => {
        const pet = pets.find(p => p.id === petId);
        return pet ? pet.name : `Pet #${petId}`;
      },
    },
    {
      title: 'Difficulty',
      dataIndex: 'difficulty',
      key: 'difficulty',
      render: (difficulty) => {
        const level = difficultyLevels.find(level => level.value === difficulty);
        return level ? (
          <Tag color={
            difficulty === 'Easy' ? 'green' :
            difficulty === 'Medium' ? 'blue' :
            difficulty === 'Hard' ? 'orange' :
            'red'
          }>
            {level.label}
          </Tag>
        ) : difficulty;
      },
    },
    {
      title: 'Score',
      dataIndex: 'score',
      key: 'score',
      render: (score) => <strong>{score}</strong>,
    },
    {
      title: 'XP Reward',
      dataIndex: 'experience_reward',
      key: 'experience_reward',
      render: (xp) => <Tag color="purple">{xp} XP</Tag>,
    },
    {
      title: 'BITS Reward',
      dataIndex: 'currency_reward',
      key: 'currency_reward',
      render: (bits) => <Tag color="gold">{bits} BITS</Tag>,
    },
    {
      title: 'Completed',
      dataIndex: 'completed_at',
      key: 'completed_at',
      render: (completedAt) => new Date(completedAt).toLocaleString(),
    },
  ];

  return (
    <div>
      <Card 
        title="Mini-Games" 
        extra={
          <Button 
            type="primary" 
            icon={<PlayCircleOutlined />} 
            onClick={() => setStartGameModalVisible(true)}
          >
            Start New Game
          </Button>
        }
        style={{ width: '100%', marginBottom: 16 }}
      >
        <Tabs defaultActiveKey="active">
          <TabPane tab="Active Games" key="active">
            {loading ? (
              <div style={{ textAlign: 'center', padding: 24 }}>
                <Spin size="large" />
                <p style={{ marginTop: 16 }}>Loading games...</p>
              </div>
            ) : (
              <Table 
                dataSource={activeGames} 
                columns={activeGamesColumns} 
                rowKey="id"
                loading={refreshing}
                pagination={false}
                locale={{ emptyText: 'No active games. Start a new game to train your pet!' }}
              />
            )}
          </TabPane>
          <TabPane tab="Completed Games" key="completed">
            {loading ? (
              <div style={{ textAlign: 'center', padding: 24 }}>
                <Spin size="large" />
                <p style={{ marginTop: 16 }}>Loading games...</p>
              </div>
            ) : (
              <Table 
                dataSource={completedGames} 
                columns={completedGamesColumns} 
                rowKey="id"
                loading={refreshing}
                pagination={{ pageSize: 5 }}
                locale={{ emptyText: 'No completed games yet. Complete a game to see your rewards!' }}
              />
            )}
          </TabPane>
        </Tabs>
      </Card>

      {/* Game Types Information */}
      <Card title="Game Types" style={{ width: '100%', marginBottom: 16 }}>
        <Row gutter={[16, 16]}>
          <Col span={8}>
            <Card>
              <Statistic
                title="Logic Leaper"
                value="Intelligence"
                prefix={<BulbOutlined style={{ color: '#722ed1' }} />}
                valueStyle={{ color: '#722ed1' }}
              />
              <p>A puzzle game that challenges your pet's problem-solving abilities. Trains Intelligence stat.</p>
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic
                title="Aura Weaving"
                value="Charisma"
                prefix={<TrophyOutlined style={{ color: '#fa8c16' }} />}
                valueStyle={{ color: '#fa8c16' }}
              />
              <p>A rhythm and pattern-matching game that enhances your pet's social skills. Trains Charisma stat.</p>
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic
                title="Habitat Dash"
                value="Agility"
                prefix={<RocketOutlined style={{ color: '#13c2c2' }} />}
                valueStyle={{ color: '#13c2c2' }}
              />
              <p>An endless runner style game that tests your pet's reflexes and speed. Trains Agility stat.</p>
            </Card>
          </Col>
        </Row>
      </Card>

      {/* Start Game Modal */}
      <Modal
        title="Start New Game"
        visible={startGameModalVisible}
        onOk={handleStartGame}
        onCancel={() => setStartGameModalVisible(false)}
        confirmLoading={actionLoading}
      >
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 8 }}>Select Pet:</label>
          <Select
            style={{ width: '100%' }}
            placeholder="Select a pet"
            value={selectedPet}
            onChange={setSelectedPet}
          >
            {pets.map(pet => (
              <Option key={pet.id} value={pet.id}>{pet.name}</Option>
            ))}
          </Select>
        </div>
        
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 8 }}>Game Type:</label>
          <Select
            style={{ width: '100%' }}
            value={selectedGameType}
            onChange={setSelectedGameType}
          >
            {gameTypes.map(type => (
              <Option key={type.value} value={type.value}>
                {type.label} - {type.description}
              </Option>
            ))}
          </Select>
        </div>
        
        <div>
          <label style={{ display: 'block', marginBottom: 8 }}>Difficulty:</label>
          <Select
            style={{ width: '100%' }}
            value={selectedDifficulty}
            onChange={setSelectedDifficulty}
          >
            {difficultyLevels.map(level => (
              <Option key={level.value} value={level.value}>
                {level.label} - {level.multiplier} rewards
              </Option>
            ))}
          </Select>
        </div>
      </Modal>

      {/* Submit Score Modal */}
      <Modal
        title="Submit Game Score"
        visible={submitScoreModalVisible}
        onOk={handleSubmitScore}
        onCancel={() => setSubmitScoreModalVisible(false)}
        confirmLoading={actionLoading}
      >
        <div>
          <label style={{ display: 'block', marginBottom: 8 }}>Your Score:</label>
          <InputNumber
            style={{ width: '100%' }}
            min={1}
            max={10000}
            value={score}
            onChange={setScore}
          />
          <p style={{ marginTop: 8, color: '#8c8c8c' }}>
            <ClockCircleOutlined /> Higher scores will earn more XP and BITS rewards!
          </p>
        </div>
      </Modal>
    </div>
  );
};

export default MinigamesPanel;