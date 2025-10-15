from fastapi import FastAPI
from app.routers import ticket, schedule, user, tickets_priority, customer, tickets_status, announcement, nps, position, ticket_category, ticket_type, user_type, vehicle_brand, vehicle_model, vehicle, auth
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

from app.models.ticket import Ticket

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
app.include_router(schedule.router)

# Lista explícita de orígenes que pueden llamar a tu API
ALLOWED_ORIGINS = [
    "http://localhost:5173",      # Vite
    "http://localhost:3000",      # Alternativa local
    "https://smarttechnical.up.railway.app",       # dominio de prod del front
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,                         # no uses "*" si allow_credentials=True
    allow_credentials=True,                                # en true si usas cookies/sesiones
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With", "Accept"],
    expose_headers=["Content-Disposition"],                # opcional
    max_age=600,                                           # cache del preflight
)