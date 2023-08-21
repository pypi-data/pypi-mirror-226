from dataclasses import dataclass

@dataclass
class Service:
    service: str
    name: str
    type: str
    rate: str
    min: str
    max: str
    dripfeed: bool
    refill: bool
    cancel: bool
    category: str
    description: str
    time: str
    admin_cost: str = None
    
@dataclass
class OrderStatus:
    order_id: str
    charge: str
    status: str
    remains: str