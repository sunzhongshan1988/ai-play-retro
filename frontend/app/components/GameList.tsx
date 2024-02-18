'use client'

import React from 'react';
import useSWR from 'swr';
import { List, Avatar, Typography, Button, message } from 'antd';
import { Game, GameListProps } from '../interfaces/Game';

const { Text } = Typography;



const fetcher = (url: string) => fetch(url).then(res => res.json());

const GameList: React.FC<GameListProps> = ({ platform }) => {
  const [messageApi, contextHolder] = message.useMessage();

  const [currentGame, setCurrentGame] = React.useState<string | null>(null);
  const [kaneRunning, setKaneRunning] = React.useState<boolean>(false);
  const [abelRunning, setAbelRunning] = React.useState<boolean>(false);

  const { data, error, isLoading } = useSWR<{ games: Game[] }>(`http://localhost:8000/games?platform=${platform}`, fetcher);

  if (error) return <div>Load Error</div>;
  if (isLoading) return <div>Loading...</div>;

  const playGame = async (game: string, ai: string) => {
    try {
      const response = await fetch('http://localhost:8000/play', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          platform,
          game,
          ai,
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      messageApi.success('Run game success');
      setKaneRunning(ai === 'kane');
      setAbelRunning(ai === 'abel');

    } catch (error) {
      messageApi.error('Run game failed');
    }
  }

  const stopGame = async (ai: string) => {
    try {
      const response = await fetch('http://localhost:8000/stop', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ai,
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      messageApi.success('Stop game success');

      ai === 'kane' && setKaneRunning(false);
      ai === 'abel' && setAbelRunning(false);

    } catch (error) {
      messageApi.error('Stop game failed');
    }
  }

  const clickKane = async (game: string) => {
    if (kaneRunning) {
      await stopGame('kane');
    } else {
      await playGame(game, 'kane');
      setCurrentGame(game);
    }
  }

  const clickAbel = async (game: string) => {
    if (abelRunning) {
      await stopGame('abel');
    } else {
      await playGame(game, 'abel');
      setCurrentGame(game);
    }
  }

  return (
    <>
      { contextHolder }
      <List
      itemLayout="horizontal"
      dataSource={data?.games}
      renderItem={item => (
        <List.Item
          key={item.key}
          actions={[
            <Button key="kane" onClick={() => clickKane(item.key)}>
              {kaneRunning ? 'Stop Kane' : 'Run Kane'}
            </Button>,
            <Button key="abel" onClick={() => clickAbel(item.key)}>
              {abelRunning ? 'Stop Abel' : 'Run Abel'}
            </Button>
          ]}
        >
          <List.Item.Meta
            avatar={<Avatar size="large" src={`${item.key}.svg`}/>}
            title={<span>{item.name}</span>}
            description={
              <Text
                style={{ width: '100%' }}
                ellipsis={{ tooltip: item.description }}
              >
                {item.description}
              </Text>}
          />
        </List.Item>
      )}
    />
    </>
  );
};

export default GameList;

