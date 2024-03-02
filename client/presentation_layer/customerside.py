from fastapi import FastAPI, HTTPException, BackgroundTasks, Body, Response, Request
from fastapi.responses import JSONResponse
from presentation_layer.models import DecisionPlModel
import json
from business_logic_layer.bll import BusinessLogicLayer
from business_logic_layer.models import Orders, Order
# from business_logic_layer.message_queues import envoyer_message_a_queue
app = FastAPI()


@app.put("/order_decision/{customer_number}")
async def order_decision(customer_number: str, order_decision: DecisionPlModel = Body()):
    decision = order_decision.model_dump()
    BusinessLogicLayer.update_order_decision(customer_number, decision)
    return {"message": "Votre décision a été bien reçu"}


@app.put("/order_devis/{customer_number}")
async def order_decision(customer_number: str, order_decision: DecisionPlModel = Body()):
    decision = order_decision.model_dump()
    BusinessLogicLayer.update_order_decision(customer_number, decision)
    return {"message": "Votre décision a été bien reçu"}


@app.put("/order_facture/{customer_number}")
async def order_decision(customer_number: str, order_decision: DecisionPlModel = Body()):
    decision = order_decision.model_dump()
    BusinessLogicLayer.update_order_decision(customer_number, decision)
    return {"message": "Votre décision a été bien reçu"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
