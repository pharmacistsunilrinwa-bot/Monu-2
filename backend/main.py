from fastapi import FastAPI, Depends, HTTPException, status
import asyncio
from services.orchestration_service import OrchestrationService
from services.provider_registry import ProviderRegistryService
from services.economic_task_engine import EconomicTaskEngine, MockAuthService
from services.monitoring_services import HealthMonitorService
from deployment.manager import DeploymentManager
from security.audit_logger import AuditLogger
from security.owner_bond import OwnerBondService
from security.vault import Vault
from security.rate_limiter import RateLimitMiddleware
from core.event_bus import EventBus
from core.task_queue import TaskQueue
from auth import get_current_user
from backend.config.config_loader import Config

app = FastAPI()
app.add_middleware(RateLimitMiddleware)

# Integrated Core
vault = Vault()
orchestrator = OrchestrationService()
provider_registry = ProviderRegistryService()
economic_engine = EconomicTaskEngine(MockAuthService())
deployment_manager = DeploymentManager(AuditLogger())
owner_bond = OwnerBondService(vault)
health_monitor = HealthMonitorService()
event_bus = EventBus()
task_queue = TaskQueue()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(task_queue.worker())

# Security settings
EMERGENCY_MODE = False
VERSION = Config.get("VERSION")

def check_emergency_mode():
    if EMERGENCY_MODE:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Emergency security mode active.")

@app.get("/health")
async def get_health():
    return health_monitor.get_health()

@app.post("/code/analyze")
async def analyze_code(request: dict, current_user: dict = Depends(get_current_user)):
    check_emergency_mode()
    return deployment_manager.analyze_and_propose(
        current_user["username"], 
        request["patch_id"], 
        request["file_path"], 
        request["fix_logic"]
    )

@app.get("/version")
async def get_version():
    return {"version": VERSION}

@app.post("/emergency/toggle")
async def toggle_emergency(current_user: dict = Depends(get_current_user)):
    global EMERGENCY_MODE
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    EMERGENCY_MODE = not EMERGENCY_MODE
    return {"emergency_mode": EMERGENCY_MODE}

@app.post("/chat")
async def chat(request: dict, current_user: dict = Depends(get_current_user)):
    check_emergency_mode()
    return await orchestrator.handle_request(request["message"])

@app.post("/economic/task")
async def economic_task(task_id: str, action: str, current_user: dict = Depends(get_current_user)):
    check_emergency_mode()
    # High-security requirement
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="High-security access required.")
        
    if action == "execute":
        return economic_engine.execute(task_id)
    return {"status": "INVALID_ACTION"}
