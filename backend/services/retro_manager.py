import asyncio
from multiprocessing import Process, Queue
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict

# 假设的 AI 类
from ais.kane.kane import Kane
from ais.abel.abel import Abel

class RetroManager:
    '''
    确保了跨进程通信数据能够被异步地处理并通过 WebSocket 发送到客户端，
    而不会阻塞 FastAPI 的主事件循环。
    通过在 transfer_and_send 方法中增加了一个简单的轮询机制（并通过 await asyncio.sleep(0.01) 释放控制权），
    使得其他协程有机会运行，从而提高了整体的异步性能。
    '''
    def __init__(self):
        self.retro: Dict[str, Process] = {}
        self.mp_queues: Dict[str, Queue] = {}  # 存储与每个游戏实例关联的 multiprocessing.Queue
        self.async_queues: Dict[str, asyncio.Queue] = {}  # 存储与每个游戏实例关联的 asyncio.Queue
        self.connections: Dict[str, WebSocket] = {}  # WebSocket 连接

    def start_retro(self, ai, game_id, ws: WebSocket):
        if ai in self.retro:
            print(f"AI {ai} is already running.")
            return "AI {ai} is already running."
        
        mp_queue = Queue()
        async_queue = asyncio.Queue()
        self.mp_queues[ai] = mp_queue
        self.async_queues[ai] = async_queue
        self.connections[ai] = ws  # 存储 WebSocket 连接
        
        if ai == "abel":
            p = Process(target=self.run_ai, args=(Abel, game_id, mp_queue))
        else:
            p = Process(target=self.run_ai, args=(Kane, game_id, mp_queue))
        
        p.start()
        self.retro[ai] = p

        # 在主进程中异步处理队列中的数据
        asyncio.create_task(self.transfer_and_send(ai))

    @staticmethod
    def run_ai(ai_class, game_id, queue):
        ai_instance = ai_class(game_id, queue)
        ai_instance.run()

    async def transfer_and_send(self, ai):
        mp_queue = self.mp_queues[ai]
        async_queue = self.async_queues[ai]
        ws = self.connections[ai]
        while True:
            if not mp_queue.empty():
                message = mp_queue.get()
                await async_queue.put(message)

            if not async_queue.empty():
                message = await async_queue.get()
                try:
                    await ws.send_json(message)
                except WebSocketDisconnect:
                    self.stop_retro(ai)
                    break
            else:
                await asyncio.sleep(0.01)  # 避免密集轮询

    def stop_retro(self, ai):
        if ai in self.retro:
            process = self.retro[ai]
            process.terminate()
            process.join()
            del self.retro[ai]
            del self.mp_queues[ai]
            del self.async_queues[ai]
            del self.connections[ai]  # 注销 WebSocket 连接
            print(f"AI {ai} stopped.")
        else:
            print(f"AI {ai} not running.")

retro_manager = RetroManager()
