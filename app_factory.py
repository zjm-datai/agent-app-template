import time
import logging
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from contextlib import asynccontextmanager

from extensions import (
    ext_database,
)

EXTENSIONS = [
    ext_database,
]

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request.state.request_id = int(time.time() * 1000)
        response = await call_next(request)
        response.headers["X-Request-ID"] = str(request.state.request_id)
        return response

def create_app() -> FastAPI:
    """
    用 lifespan 把启动/关闭逻辑都集中在一个地方。
    """
    # 先创建应用实例
    app = FastAPI()
    
    # 在应用启动前注册中间件
    app.add_middleware(RequestIDMiddleware)
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # —— startup 阶段 —— #
        start = time.perf_counter()

        # 初始化每个扩展的“启动”部分
        for ext in EXTENSIONS:
            if hasattr(ext, "is_enabled") and not ext.is_enabled():
                logging.info(f"Skipped extension {ext.__name__}")
                continue
            t0 = time.perf_counter()
            # 约定：每个 ext 模块都提供 init_app()，做启动阶段的工作
            ext.init_app(app)
            t1 = time.perf_counter()
            # logging.info(f"Loaded {ext.__name__} in {(t1 - t0) * 1000:.2f}ms")
            print(f"Loaded {ext.__name__} in {(t1 - t0) * 1000:.2f}ms")
        end = time.perf_counter()
        
        # logging.info(f"Application startup finished in {(end - start)*1000:.2f}ms")

        print(f"Application startup finished in {(end - start)*1000:.2f}ms")

        print("engine in lifespan:", app.state.engine)

        yield  # —— 业务请求处理阶段 —— #

        # —— shutdown 阶段 —— #
        # 如果有需要清理的资源，可以在各自 ext 模块里定义 shutdown_app()
        for ext in reversed(EXTENSIONS):
            if hasattr(ext, "shutdown_app"):
                # await ext.shutdown_app(app)
                ext.shutdown_app(app)
        logging.info("Application shutdown complete")
    
    # 为应用设置 lifespan
    app = FastAPI(lifespan=lifespan)
    
    return app