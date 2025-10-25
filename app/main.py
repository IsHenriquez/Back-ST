from fastapi import FastAPI, Response
from app.routers import ticket, schedule, user, tickets_priority, customer, tickets_status, announcement, nps, position, ticket_category, ticket_type, user_type, vehicle_brand, vehicle_model, vehicle, auth
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware
import time

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


# Métricas
REQUEST_COUNT = Counter(
    "http_requests_total", "Total de requests", ["method", "endpoint", "http_status"]
)
REQ_LATENCY = Histogram(
    "http_request_duration_seconds", "Latencia de requests", ["method", "endpoint"]
)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        endpoint = request.url.path
        method = request.method
        REQ_LATENCY.labels(method, endpoint).observe(time.perf_counter() - start)
        REQUEST_COUNT.labels(method, endpoint, str(response.status_code)).inc()
        return response

# middleware de métricas
app.add_middleware(MetricsMiddleware)

# Endpoint para Prometheus
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
