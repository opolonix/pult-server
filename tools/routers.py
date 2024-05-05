import os, fastapi

def include_routers(app: fastapi.FastAPI, path: str, router: str = "router"):
    
    for file in os.listdir(path):
        if file.endswith(".py"):
            module = __import__(f"{path}.{file[:-3]}", fromlist=["router"])
            if hasattr(module, router):
                app.include_router(getattr(module, router))