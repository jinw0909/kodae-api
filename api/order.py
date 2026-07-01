from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/order/create")
def create_order_api(user_id: int, product_id: int, db: Session = Depends(get_db)):

    user = db.query(User).get(user_id)
    product = db.query(Product).get(product_id)

    result = create_payment_flow(db, user, product)

    return result