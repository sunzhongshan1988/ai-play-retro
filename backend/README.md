
# Dependencies

Apple Silicon must be manually install `stable-retro` see here: [https://github.com/Farama-Foundation/stable-retro](https://github.com/Farama-Foundation/stable-retro)

# Running

About windows platform, you must be running in WSL2.

```bash
cd backend
uvicorn main:app --reload
```

# train model

```bash
cd backend
python train.py game-name
```
