import asyncio
from fastapi import FastAPI, WebSocket, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.websockets import WebSocketDisconnect
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from tools import compress_response
app = FastAPI(docs_url="/docs")

templates = Jinja2Templates(directory="templates")

app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(GZipMiddleware, minimum_size=1000)

allowed_hosts = ["www.example.com", "example.com", "127.0.0.1"]
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)


@app.get("/")
async def get_chat(request: Request):
    return templates.TemplateResponse(
        request=request, name="websocket_client.html"
    )

@app.middleware("https")
async def middleware(request: Request, call_next):
    response = await call_next(request)
    url = str(request.url.path)

    exempt_urls = ["/", "/docs", "/openapi.json"]
    if url not in exempt_urls:
        body = b"".join([chunk async for chunk in response.body_iterator])
        if len(body) >= 1000:
            compressed_body = compress_response(body.decode('utf-8'))
            response = Response(
                content=compressed_body,
                status_code=response.status_code,
            )


    return response


@app.get("/large_text")
async def large_text(user: str = "Anonimus"):
    return user * 1000



@app.get("/hello")
async def hello_rout(user: str = "Anonimus"):
    await asyncio.sleep(0.1)
    return f"Hello, {user}!"


# Життєвий Цикл WebSocket-З'єднання:
@app.websocket("/ws/base")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Ініціалізація (Handshake)
    print("Connect raise")
    try:
        while True:  # Трансфер Даних
            data = await websocket.receive_text()
            print(data)
            await websocket.send_text(f" Server get message: {data}")

    except WebSocketDisconnect:  # Управління З'єднанням
        print("Client raise disconnect")
    except Exception as e:
        print(f"Critical Error: {e}")

    finally:  # Закриття З'єднання
        if not websocket.client_state.DISCONNECTED:
            await websocket.close()


if __name__ == "__main__":
    from server_run import uvicorn_run

    # hypercorn_run(app)
    uvicorn_run()
