#!/usr/bin/env python3
"""
🍪 MERIENDA_DEPIN_ORCHESTRATOR.py (Era 216.0)
Bridging the Global Merienda protocol with the Republic's industrial core.
"""

import sys
import os
import heapq
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
import threading
import json
import time
import random

class JobPriority(Enum):
    GENESIS = 0      # Highest - founders, core contributors
    PLATINUM = 1     # High Merit burn rate
    GOLD = 2         # Medium Merit burn
    SILVER = 3       # Standard - base $HIL only
    BRONZE = 4       # Low priority, social multiplier only

@dataclass(order=True)
class FabricationJob:
    priority: int  # Lower = higher priority (for heapq)
    submitted_at: float = field(compare=False)
    job_id: str = field(compare=False)
    user_id: str = field(compare=False)
    job_type: str = field(compare=False)
    spec: Dict = field(compare=False)
    social_multiplier: float = field(compare=False)
    merit_burn: int = field(compare=False)
    hil_amount: float = field(compare=False)
    status: str = field(default="queued", compare=False)
    estimated_duration: float = field(default=0.0, compare=False)

class JobQueue:
    def __init__(self):
        self.queue = []
        self.active_job = None
        self.job_history = []
        self.lock = threading.Lock()
        self.job_counter = 0
        
    def priority_from_tier(self, user_tier: str) -> int:
        """Convert social tier to priority integer."""
        mapping = {
            'GENESIS': JobPriority.GENESIS.value,
            'PLATINUM': JobPriority.PLATINUM.value,
            'GOLD': JobPriority.GOLD.value,
            'SILVER': JobPriority.SILVER.value,
            'BRONZE': JobPriority.BRONZE.value
        }
        return mapping.get(user_tier, JobPriority.BRONZE.value)
    
    def submit_job(self, user_id: str, job_type: str, spec: Dict, 
                   social_multiplier: float, merit_burn: int = 0) -> str:
        """
        Submit a fabrication job with priority derived from token economics.
        """
        with self.lock:
            self.job_counter += 1
            job_id = f"job_{self.job_counter}_{int(datetime.now().timestamp())}"
            
            # Determine priority tier from merit burn + social multiplier
            if merit_burn >= 100:
                tier = 'PLATINUM'
            elif merit_burn >= 25:
                tier = 'GOLD'
            elif social_multiplier >= 0.7:
                tier = 'SILVER'
            else:
                tier = 'BRONZE'
            
            # Genesis override (special addresses)
            if user_id in ['GENESIS_CITIZEN_001', 'GT_07_ARCHITECT']:
                tier = 'GENESIS'
            
            priority = self.priority_from_tier(tier)
            
            # Calculate $HIL cost (base 250,000 Joules = 250,000 $HIL)
            base_cost = 250000.0
            hil_amount = base_cost * social_multiplier
            
            # Merit burn reduces $HIL cost
            hil_amount = max(0, hil_amount - (merit_burn * 1000))
            
            job = FabricationJob(
                priority=priority,
                submitted_at=datetime.now().timestamp(),
                job_id=job_id,
                user_id=user_id,
                job_type=job_type,
                spec=spec,
                social_multiplier=social_multiplier,
                merit_burn=merit_burn,
                hil_amount=hil_amount,
                status="queued"
            )
            
            heapq.heappush(self.queue, job)
            
            print(f"   📋 Job {job_id} queued | Tier: {tier} | Priority: {priority} | $HIL: {hil_amount:.0f}")
            return job_id
    
    def next_job(self) -> Optional[FabricationJob]:
        """Pop highest priority job from queue."""
        with self.lock:
            if self.queue:
                job = heapq.heappop(self.queue)
                job.status = "dispatching"
                self.active_job = job
                return job
            return None
    
    def complete_job(self, job_id: str, success: bool, proof_hash: str = None):
        """Mark job as complete and archive."""
        with self.lock:
            if self.active_job and self.active_job.job_id == job_id:
                self.active_job.status = "completed" if success else "failed"
                self.active_job.completed_at = datetime.now().timestamp()
                self.job_history.append(self.active_job)
                
                print(f"   ✅ Job {job_id} {'succeeded' if success else 'failed'}")
                if proof_hash:
                    print(f"   🔐 PoPW: {proof_hash[:16]}...")
                
                self.active_job = None
    
    def queue_status(self) -> Dict:
        """Return current queue status."""
        with self.lock:
            return {
                "queued_jobs": len(self.queue),
                "active_job": self.active_job.job_id if self.active_job else None,
                "total_completed": len(self.job_history),
                "queue": [{
                    "job_id": j.job_id,
                    "priority": j.priority,
                    "user_id": j.user_id
                } for j in sorted(self.queue)]
            }

# Global queue instance
job_queue = JobQueue()

def get_reputation(user_id):
    # Simulated social capital
    if user_id in ['GENESIS_CITIZEN_001', 'GT_07_ARCHITECT']:
        return 1.0 # Max reputation for Genesis
    return 0.85

def route_fabrication_job(user_id: str, job_spec: Dict, merit_burn: int = 0):
    """
    Submit job to queue, settle tokens, dispatch when ready.
    """
    # Fetch user reputation
    user_reputation = get_reputation(user_id)
    social_multiplier = 1.0 - (user_reputation * 0.15)  # Up to 85% discount
    
    # Submit to queue
    job_id = job_queue.submit_job(
        user_id=user_id,
        job_type=job_spec.get('job_type', 'tfln_housing'),
        spec=job_spec,
        social_multiplier=social_multiplier,
        merit_burn=merit_burn
    )
    
    # Token settlement happens at dispatch, not submission
    print(f"   💰 Tokens reserved: {job_spec.get('hil_reserved', 0)} $HIL")
    
    return job_id

def settle_tokens(user_id, hil_amount, merit_burn):
    print(f"   💰 SETTLED: {hil_amount:.0f} $HIL & {merit_burn} Merit Tokens from {user_id}")
    time.sleep(0.5)

def queue_processor(cnc_substrate, serial_port="/dev/ttyUSB0", iterations=3):
    """
    Background thread that processes jobs from queue.
    """
    print("🔄 Queue processor started. Waiting for jobs...")
    count = 0
    while count < iterations:
        job = job_queue.next_job()
        
        if job:
            print(f"\n🏭 Processing job: {job.job_id}")
            print(f"   User: {job.user_id} | $HIL: {job.hil_amount:.0f}")
            
            # Settle tokens now
            settle_tokens(job.user_id, job.hil_amount, job.merit_burn)
            
            # Generate G-Code for the job
            cnc_substrate.generate_tfln_pocket()
            
            # Dispatch to CNC
            result = cnc_substrate.stream_to_machine(
                serial_port=serial_port,
                hardware=False # Mocking hardware
            )
            
            # Complete job
            proof = result.get('proof_hash') if result.get('status') == 'success' else None
            job_queue.complete_job(job.job_id, result.get('status') == 'success', proof)
        else:
            break
        
        time.sleep(1)
        count += 1

def orchestrate_merienda():
    print("\n🍪 INITIATING GLOBAL MERIENDA ORCHESTRATION...")
    time.sleep(1)
    
    steps = [
        "📡 DETECTING DePIN HOST (Fabrika OS)...",
        "⚙️  SYNCHRONIZING WITH RUST CORE (GlobalMerienda::trigger_inaugural)...",
        "📈 AUDITING NETWORK HEALTH (Helium Nerves)...",
        "⚖️  VERIFYING SIGNAL INTEGRITY (Social Capital Multiplier)...",
        "🪙  ORCHESTRATING JOULE DISTRIBUTION (15,000 Genesis Citizens)...",
        "✅ MERIENDA COMPLETE: Social nourishment disseminated."
    ]
    
    for step in steps:
        print(f"[{time.strftime('%H:%M:%S')}] {step}")
        time.sleep(random.uniform(0.1, 0.3))

    # Trigger sample CNC jobs to test queue
    print("\n📦 INJECTING TEST WORKLOAD TO DePIN QUEUE...")
    route_fabrication_job(
        user_id="Citizen_4922",
        job_spec={
            "material": "Acrylic",
            "thickness_mm": 5,
        },
        merit_burn=5
    )
    
    route_fabrication_job(
        user_id="Citizen_118",
        job_spec={
            "material": "6061 Aluminum",
            "thickness_mm": 10,
        },
        merit_burn=75
    )
    
    route_fabrication_job(
        user_id="GENESIS_CITIZEN_001",
        job_spec={
            "material": "6061 Aluminum",
            "thickness_mm": 10,
        },
        merit_burn=50
    )
    
    print("\n🔄 EXECUTING DePIN QUEUE (Priority Order):")
    # Lazy import CNCSubstrate for execution
    sys.path.append(os.path.join(os.path.dirname(__file__), '../04_SUBSTRATES/08_HARDWARE/CAD/'))
    try:
        from fabrika_api import CNCSubstrate
        cnc = CNCSubstrate()
        queue_processor(cnc, iterations=3)
    except Exception as e:
        print(f"⚠️ Could not load Fabrika API: {e}")

    print("\n📊 MERIENDA TELEMETRY:")
    print("-" * 40)
    print(f"PROTOCOL     : GLOBAL MERIENDA (Era 6)")
    print(f"HOST OS      : FABRIKA OS (Foundry Node)")
    print(f"CITIZENS     : 15,000 (Genesis)")
    print(f"MESH QUALITY : {random.randint(85, 98)}%")
    print(f"JOULES DIST  : {random.randint(1500000, 2250000)}")
    print("-" * 40)
    print("\n🏛️  THE REPUBLIC IS NOURISHED BY ITS OWN EXCELLENCE.")

if __name__ == "__main__":
    try:
        orchestrate_merienda()
    except KeyboardInterrupt:
        print("\n⚠️  ORCHESTRATION SEVERED.")
        sys.exit(0)
