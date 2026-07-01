from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
import hmac
import hashlib
import json
from datetime import datetime
from zoneinfo import ZoneInfo

from db.session import get_db
from db.models import WebhookLog, WebhookLogHistory

router = APIRouter()

TOSS_SECRET = "test_sk_5OWRapdA8ddglyLezN0X8o1zEqZK"


def verify_signature(payload: dict, signature: str) -> bool:
    payload_str = json.dumps(
        payload,
        separators=(",", ":"),
        ensure_ascii=False
    )

    expected_signature = hmac.new(
        TOSS_SECRET.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, signature)


@router.post("/webhook/toss", summary="Toss Webhook", tags=["USER API"])
async def toss_webhook(request: Request, db: Session = Depends(get_db)):
    payload = None
    order_id = None
    payment_key = None
    status = None

    try:
        print("====================================")

        payload = await request.json()
        print(payload)

        signature = request.headers.get("Toss-Signature")

        # if not signature:
        #     raise HTTPException(status_code=400, detail="No signature")

        # if not verify_signature(payload, signature):
        #     raise HTTPException(status_code=403, detail="Invalid signature")

        event_type = payload.get("eventType")
        created_at = payload.get("createdAt")

        data = payload.get("data", {})
        payment = data.get("payment", {})

        order_id = payment.get("orderId")
        payment_key = payment.get("paymentKey")
        status = payment.get("status")
        method = payment.get("method")

        print("event_type :", event_type)
        print("order_id   :", order_id)
        print("paymentKey :", payment_key)
        print("status     :", status)

        now_kst = datetime.now(ZoneInfo("Asia/Seoul"))

        # ==================================================
        # History 저장 (무조건 저장)
        # ==================================================
        history = WebhookLogHistory(
            order_id=order_id,
            payment_key=payment_key,
            status=status,
            payload=json.dumps(payload, ensure_ascii=False),
            datetime=now_kst
        )

        db.add(history)
        db.commit()

        # ==================================================
        # 필수값 체크
        # ==================================================
        if not order_id:
            raise HTTPException(status_code=400, detail="Missing orderId")

        # ==================================================
        # 중복 체크
        # ==================================================
        exists = (
            db.query(WebhookLog)
            .filter_by(
                order_id=order_id,
                payment_key=payment_key,
                status=status
            )
            .first()
        )

        if exists:
            return {
                "ok": True,
                "message": "duplicate ignored"
            }

        # ==================================================
        # webhook_log 저장
        # ==================================================
        saved = WebhookLog(
            order_id=order_id,
            payment_key=payment_key,
            status=status,
            payload=json.dumps(payload, ensure_ascii=False),
            datetime=now_kst
        )

        db.add(saved)

        # ==================================================
        # 주문 처리
        # ==================================================

        # order = (
        #     db.query(Order)
        #     .filter_by(order_id=order_id)
        #     .first()
        # )

        # if status == "DONE":
        #     if order:
        #         order.status = "PAID"

        # elif status == "CANCELED":
        #     if order:
        #         order.status = "CANCELED"

        # elif status == "FAILED":
        #     if order:
        #         order.status = "FAILED"

        db.commit()
        db.refresh(saved)

        return {
            "ok": True,
            "id": saved.id,
            "eventType": event_type,
            "status": status
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Webhook Error :", str(e))

        db.rollback()

        try:
            error_history = WebhookLogHistory(
                order_id=order_id,
                payment_key=payment_key,
                status="ERROR",
                payload=json.dumps(
                    {
                        "error": str(e),
                        "payload": payload
                    },
                    ensure_ascii=False
                ),
                datetime=datetime.now(ZoneInfo("Asia/Seoul"))
            )

            db.add(error_history)
            db.commit()

        except Exception:
            db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )