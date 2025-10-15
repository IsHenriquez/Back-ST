from fastapi import FastAPI
from app.routers import ticket, user, tickets_priority, customer, tickets_status, announcement, nps, position, ticket_category, ticket_type, user_type, vehicle_brand, vehicle_model, vehicle, auth

app = FastAPI()

app.include_router(ticket.router)
app.include_router(user.router)
app.include_router(tickets_priority.router)
app.include_router(customer.router)
app.include_router(tickets_status.router)
app.include_router(announcement.router)
app.include_router(nps.router)
app.include_router(position.router)
app.include_router(ticket_category.router)
app.include_router(ticket_type.router)
app.include_router(user_type.router)
app.include_router(vehicle_brand.router)
app.include_router(vehicle_model.router)
app.include_router(vehicle.router)
app.include_router(auth.router)
