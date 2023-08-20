from typing import Annotated, List

from faa_utils.deps import PageSelector
from fastapi import APIRouter, Depends, Query
from fastapi_amis_admin.crud import BaseApiOut
from fastapi_amis_admin.globals.deps import SyncSess
from fastapi_user_auth.globals.deps import CurrentUser
from sqlmodel.sql.expression import SelectOfScalar

from faa_wechat.payment_base.enums import PayLogType
from faa_wechat.payment_base.models import BalanceLog, PayUser, ScoreLog

router = APIRouter()


# 获取余额日志记录列表
@router.get(
    "/get_balance_logs",
    response_model=BaseApiOut[List[BalanceLog]],
)
def get_balance_logs(
    session: SyncSess,
    user: CurrentUser,
    sel: Annotated[SelectOfScalar[BalanceLog], Depends(PageSelector(BalanceLog))],
    pay_type: Annotated[
        PayLogType,
        Query(title="日志类型", description=str(PayLogType.choices)),  # type: ignore
    ] = None,
):
    """获取余额日志记录列表"""
    if pay_type:
        sel = sel.where(BalanceLog.type == pay_type)
    sel = sel.where(BalanceLog.user_id == user.id).order_by(BalanceLog.create_time.desc())
    result = session.scalars(sel)
    items = result.all()
    return BaseApiOut(data=items)


# 获取积分日志记录列表
@router.get(
    "/get_score_logs",
    response_model=BaseApiOut[List[ScoreLog]],
)
def get_score_logs(
    session: SyncSess,
    user: CurrentUser,
    sel: Annotated[SelectOfScalar[ScoreLog], Depends(PageSelector(ScoreLog))],
    pay_type: Annotated[
        PayLogType,
        Query(title="日志类型", description=str(PayLogType.choices)),  # type: ignore
    ] = None,
):
    """获取积分日志记录列表"""
    if pay_type:
        sel = sel.where(ScoreLog.type == pay_type)
    sel = sel.where(ScoreLog.user_id == user.id).order_by(ScoreLog.create_time.desc())
    result = session.scalars(sel)
    items = result.all()
    return BaseApiOut(data=items)


# 余额转积分
@router.post(
    "/balance_to_score",
    response_model=BaseApiOut[PayUser],
)
def balance_to_score(
    session: SyncSess,
    user: CurrentUser,
    balance: Annotated[int, Query(title="余额", description="余额", gt=0)],
):
    """余额转积分. 1元=10积分"""
    # 更新用户余额
    user.update_balance(
        balance * -1,
        log=BalanceLog(type=PayLogType.CONSUME, desc=f"余额转积分，扣除{balance}元"),
    )
    # 更新用户积分
    score = balance * 10
    user.update_score(
        score,  # 1元=10积分
        log=ScoreLog(type=PayLogType.RECHARGE, desc=f"余额转积分，增加{score}积分"),
    )
    session.flush()
    return BaseApiOut(msg="转换成功", data=PayUser.from_orm(user))
