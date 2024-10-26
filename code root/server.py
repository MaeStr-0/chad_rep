from db import *
from hasher import *
import asyncio
import uuid
import websockets
import json

connections = {}  # Словарь для хранения соединений


async def handler(websocket, path):
    try:
        print("Процесс try")
        try:
            message = json.loads(await websocket.recv())
        except json.JSONDecodeError:
            print("Error decoding")
            await websocket.close()


        match message["operation"]:
            case "auth":

                print("Case auth")
                name = message["username"]
                pwd = message["password"]
                connection_id=name
                connections[connection_id]=websocket
                hash = await  hash_password(name, pwd)
                answer = await auth(name, hash)
                if answer == 1:
                    print(f"auth {connection_id} correct")
                    await websocket.send("auth success")
                    return 1
                else:
                    await print(f"auth {connection_id} incorrect")
                    websocket.send("auth denied")
                    return 0
            case "reg":
                print("Case reg")
                name = message["username"]
                pwd = message["password"]
                connection_id = name
                connections[connection_id] = websocket
                hash = await hash_password(name, pwd)
                answer = await register(name, hash)
                if answer == 1:
                    print("Reg success")
                    await websocket.send("reg success")
                    print("Success message send to client")
                    return 1
                else:
                    print("Reg denied")
                    await websocket.send("reg denied")
                    print("Denie message send to client")
                    await websocket.close()
                    connections.pop(connection_id, None)
                    return 0
            case "mes":
                sender = message["send_from"]
                receiver = message["send_to"]
                if existence_check(receiver) == "exist":
                    await websocket.send(message["text"], connections[receiver])
            # await websocket.close()

        #connection_id = name
        #connections[connection_id] = websocket
        # Сохраняем соединение в словарь
        #connections[connection_id] = websocket
        #async for message in websocket:
        #    print(f"Получено сообщение от {connection_id}: {message}")
        # Очищаем соединение из словаря при закрытии
        #connections.pop(connection_id, None)

    except websockets.exceptions.ConnectionClosedOK:
        print(f"Соединение {connection_id} закрыто")
    except websockets.exceptions.ConnectionClosedError:
        print(f"Соединение {connection_id} разорвано")
    except websockets.exceptions.ConnectionClosed:
        print(f"Соединение {connection_id} закрыто")
    except KeyboardInterrupt:
        print("Работа сервера прекращена вручную")
        for connection_id, websocket in connections.items():
            await websocket.close()
        print("Все соединения закрыты")
    except asyncio.exceptions.CancelledError:
        print("Работа асинхронных функций прервана")



    except:
        print("dgfdgfd")


# async def send_message(connection_id, message):
# if connection_id in connections:
# websocket = connections[connection_id]
# await websocket.send(message)
# else:
# print(f"Соединение с идентификатором {connection_id} не найдено")

async def main():
    port = 8765
    async with websockets.serve(handler, "212.67.15.92", port):
        print(f"Сервер запущен на ws://212.67.15.92:{port}")
        await asyncio.Future()  # Зациклить сервер


if __name__ == "__main__":
    asyncio.run(main())