import random
from asyncio import sleep


async def load_model():
    """
    Loading the ML Model
    :return:
    """
    await sleep(2)


async def predict():
    """
    Emulate the load of the model and a prediction call
    :return: Number from 0.0 to 1.0
    """
    await load_model()
    return random.random()


async def serve():
    prediction = await predict()
    return {"Hello": "World", "prediction": prediction}
