'use client'

import type { TabsProps } from 'antd';
import { ConfigProvider, theme, Tabs, Typography, Image } from 'antd';
import { useEffect, useState } from "react";
import useSWR from "swr";
import GameList from "./components/GameList";

const { Text } = Typography;

const fetcher = (url: string) => fetch(url).then((res) => res.json());

interface Platform {
  key: string;
  name: string;
}

export default function Home() {

  const [darkMode, setDarkMode] = useState(false);

  const [kaneImage, setKaneImage] = useState('');
  const [abelImage, setAbelImage] = useState('');

  const { data, error, isLoading } = useSWR(
    "http://127.0.0.1:8000/platforms",
    fetcher
  );

  useEffect(() => {
    const windowQuery = window.matchMedia("(prefers-color-scheme: dark)");

    const darkModeChange = (event: MediaQueryListEvent) => {
      console.log(event.matches ? true : false);
      setDarkMode(event.matches);
    };

    windowQuery.addEventListener("change", darkModeChange);

    // Set the initial dark mode
    setDarkMode(windowQuery.matches);

    return () => {
      windowQuery.removeEventListener("change", darkModeChange);
    };
  }, []);


  // Websocket connection
  useEffect(() => {
    // Create a new WebSocket connection
    const ws = new WebSocket('ws://localhost:8000/ws');

    // Listen for the connection open event
    ws.onopen = () => {
      console.log('WebSocket is open now.');
    };

    // Listen for messages
    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        if (message.type === 'image' && message.ai === 'kane') {
          setKaneImage(`data:image/png;base64,${message.data}`);
        }
        if (message.type === 'image' && message.ai === 'abel') {
          setAbelImage(`data:image/png;base64,${message.data}`);
        }
      }
      catch (e) {
        console.error('WS Invalid JSON', e);
      }
    };

    // Listen for errors
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    // Listen for the connection close event
    ws.onclose = () => {
      console.log('WebSocket is closed now.');
    };

    // Close the connection when the component is unmounted
    return () => {
      ws.close();
    };
  }, []);

  
  const onChange = (key: string) => {
    console.log(key);
  };

  // Generate the tabs based on the data
  const items: TabsProps['items'] = data?.platforms?.map((platform: Platform) => ({
    key: platform, 
    label: platform.name,
    children: <GameList platform={platform.key} />,
  })) || [];


  return (
    <ConfigProvider
      theme={{
        // Use the dark theme for the algorithm component
        algorithm: darkMode ? theme.darkAlgorithm : theme.compactAlgorithm
      }}
    >
      <main className="flex min-h-screen flex-col justify-start p-24">
        <div className="flex">
          <div className="w-1/2 p-4 flex flex-col items-center">
            <Image
              src={kaneImage}
              alt="Kane"
              width={200}
              height={200}
            />
            <Text>Kane</Text>
          </div>
          <div className="w-1/2 p-4 flex flex-col items-center">
            <Image
              src={abelImage}
              alt="Abel"
              width={200}
              height={200}
            />
            <Text className="text-center">Abel</Text>
          </div>
        </div>
        <Tabs
          defaultActiveKey="1"
          items={items}
          onChange={onChange}
        />
      </main>
    </ConfigProvider>
  );
}
