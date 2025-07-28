from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.app.api.routes.auth import login_for_access_token
from backend.app.core.dependencies import db_dependency
from backend.app.core.security import get_current_user
from backend.app.models.ticket import Ticket
from backend.app.models.user import User
from backend.app.schemas.ticket import CreateTicket, ReadTicket, UpdateTicketStatus

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)

@router.get('/get', status_code=200, response_model=List[ReadTicket])
async def get_tickets(db: db_dependency):
    results = await db.execute(select(Ticket).options(selectinload(Ticket.user)))
    tickets = results.scalars().all()
    if not tickets:
        return HTTPException(status_code=404, detail="Tickets not found")
    return tickets


@router.post('/create', status_code=201)
async def create_ticket(
        db: db_dependency,
        request: CreateTicket,
        current_user: User = Depends(get_current_user)):

    ticket = Ticket(
        user_id = current_user["id"],
        title = request.title,
        description = request.description,
        created_at = datetime.now()
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.get('/get{ticket_id}', status_code=200, response_model=ReadTicket)
async def get_ticket(db: db_dependency, ticket_id: int):
    result = await db.execute(select(Ticket).options(selectinload(Ticket.user)).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.put('update/{ticket_id}', status_code=200)
async def update_ticket(
        db:db_dependency,
        ticket_id: int,
        request : CreateTicket):

    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.title = request.title
    ticket.description = request.description
    ticket.updated_at = datetime.now()

    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.patch('/update/{ticket_id}/status', status_code=200)
async def update_ticket_status(db: db_dependency, ticket_id: int, ticket_status_request: UpdateTicketStatus):
    ticket = await get_ticket(db, ticket_id)
    if not ticket:
        return HTTPException(status_code=404, detail="Ticket not found")
    ticket.status = ticket_status_request.status

    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.delete('/delete/{ticket_id}')
async def delete_ticket(db: db_dependency, ticket_id: int):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    await db.delete(ticket)
    await db.commit()
    return {"message": "Ticket deleted successfully"}
