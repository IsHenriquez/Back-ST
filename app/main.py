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
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "capacitor://localhost",
    "ionic://localhost",
    "https://smarttechnical.up.railway.app",  # tu front en prod (si aplica)
]

# Regex permisivo para orígenes locales
ALLOW_ORIGIN_REGEX = r"^(https?://localhost(:\d+)?|http://127\.0\.0\.1(:\d+)?|capacitor://localhost|ionic://localhost|https://smarttechnical\.up\.railway\.app)$"

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=ALLOW_ORIGIN_REGEX,   # <- clave para apps híbridas
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With", "Accept"],
    expose_headers=["Content-Disposition"],
    max_age=600,
)
