'use client'

import Image from "next/image";
import type { TabsProps } from 'antd';
import { ConfigProvider, theme, Tabs } from 'antd';
import { useEffect, useState } from "react";

export default function Home() {

  const [darkMode, setDarkMode] = useState(false);

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

  
  const onChange = (key: string) => {
    console.log(key);
  };

  const items: TabsProps['items'] = [
    {
      key: '1',
      label: 'Tab 1',
      children: 'Content of Tab Pane 1',
    },
    {
      key: '2',
      label: 'Tab 2',
      children: 'Content of Tab Pane 2',
    },
    {
      key: '3',
      label: 'Tab 3',
      children: 'Content of Tab Pane 3',
    },
  ];


  return (
    <ConfigProvider
      theme={{
        // Use the dark theme for the algorithm component
        algorithm: darkMode ? theme.darkAlgorithm : theme.compactAlgorithm
      }}
    >
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <Tabs defaultActiveKey="1" items={items} onChange={onChange} />
      </main>
    </ConfigProvider>
  );
}
