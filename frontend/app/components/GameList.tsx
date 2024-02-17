'use client'

import React from 'react';
import useSWR from 'swr';
import { List, Avatar, Typography, Button, message } from 'antd';
import { Game, GameListProps } from '../interfaces/Game';

const { Text } = Typography;



const fetcher = (url: string) => fetch(url).then(res => res.json());

const GameList: React.FC<GameListProps> = ({ platform }) => {
  const [messageApi, contextHolder] = message.useMessage();

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

    } catch (error) {
      messageApi.error('Run game failed');
    }
  }

  const clickKane = async (game: string) => {
    await playGame(game, 'kane');
  }

  const clickAbel = async (game: string) => {
    await playGame(game, 'abel');
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
            <Button key="kane" onClick={() => clickKane(item.key)}>Kane</Button>,
            <Button key="abel" onClick={() => clickAbel(item.key)}>Abel</Button>
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

