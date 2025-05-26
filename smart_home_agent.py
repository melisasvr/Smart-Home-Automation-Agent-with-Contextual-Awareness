"""
Smart Home Automation Agent with Contextual Awareness
Simplified version that works without complex MCP dependencies
"""

import json
import asyncio
from datetime import datetime, time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class DeviceType(Enum):
    LIGHT = "light"
    THERMOSTAT = "thermostat"
    SECURITY_CAMERA = "security_camera"
    DOOR_LOCK = "door_lock"
    MOTION_SENSOR = "motion_sensor"

class DeviceStatus(Enum):
    ON = "on"
    OFF = "off"
    ACTIVE = "active"
    INACTIVE = "inactive"

@dataclass
class Device:
    id: str
    name: str
    type: DeviceType
    status: DeviceStatus
    location: str
    properties: Dict[str, Any]
    last_updated: datetime

@dataclass
class ContextualRule:
    id: str
    name: str
    trigger_conditions: Dict[str, Any]
    actions: List[Dict[str, Any]]
    enabled: bool
    priority: int

class SmartHomeAgent:
    def __init__(self):
        self.devices: Dict[str, Device] = {}
        self.contextual_rules: Dict[str, ContextualRule] = {}
        self.user_preferences: Dict[str, Any] = {}
        self.occupancy_status: Dict[str, bool] = {}
        self.setup_default_devices()
        self.setup_default_rules()
        print("🏠 Smart Home Agent initialized successfully!")
    
    def setup_default_devices(self):
        """Initialize default smart home devices"""
        default_devices = [
            Device(
                id="living_room_light",
                name="Living Room Light",
                type=DeviceType.LIGHT,
                status=DeviceStatus.OFF,
                location="living_room",
                properties={"brightness": 0, "color": "white", "temperature": 3000},
                last_updated=datetime.now()
            ),
            Device(
                id="bedroom_light",
                name="Bedroom Light",
                type=DeviceType.LIGHT,
                status=DeviceStatus.OFF,
                location="bedroom",
                properties={"brightness": 0, "color": "white", "temperature": 3000},
                last_updated=datetime.now()
            ),
            Device(
                id="kitchen_light",
                name="Kitchen Light",
                type=DeviceType.LIGHT,
                status=DeviceStatus.OFF,
                location="kitchen",
                properties={"brightness": 0, "color": "white", "temperature": 4000},
                last_updated=datetime.now()
            ),
            Device(
                id="main_thermostat",
                name="Main Thermostat",
                type=DeviceType.THERMOSTAT,
                status=DeviceStatus.ACTIVE,
                location="hallway",
                properties={"temperature": 72, "target_temp": 72, "mode": "auto", "humidity": 45},
                last_updated=datetime.now()
            ),
            Device(
                id="front_door_camera",
                name="Front Door Camera",
                type=DeviceType.SECURITY_CAMERA,
                status=DeviceStatus.ACTIVE,
                location="front_door",
                properties={"recording": True, "motion_detection": True, "night_vision": True},
                last_updated=datetime.now()
            ),
            Device(
                id="back_door_camera",
                name="Back Door Camera",
                type=DeviceType.SECURITY_CAMERA,
                status=DeviceStatus.ACTIVE,
                location="back_door",
                properties={"recording": False, "motion_detection": True, "night_vision": True},
                last_updated=datetime.now()
            ),
            Device(
                id="front_door_lock",
                name="Front Door Lock",
                type=DeviceType.DOOR_LOCK,
                status=DeviceStatus.OFF,  # OFF = locked
                location="front_door",
                properties={"locked": True, "auto_lock": True, "access_code": "1234"},
                last_updated=datetime.now()
            ),
            Device(
                id="living_room_motion",
                name="Living Room Motion Sensor",
                type=DeviceType.MOTION_SENSOR,
                status=DeviceStatus.INACTIVE,
                location="living_room",
                properties={"sensitivity": "medium", "last_motion": None},
                last_updated=datetime.now()
            )
        ]
        
        for device in default_devices:
            self.devices[device.id] = device
    
    def setup_default_rules(self):
        """Setup default contextual automation rules"""
        default_rules = [
            ContextualRule(
                id="welcome_home",
                name="Welcome Home Automation",
                trigger_conditions={
                    "door_unlock": True,
                    "time_range": {"start": "06:00", "end": "22:00"}
                },
                actions=[
                    {"device_id": "living_room_light", "action": "turn_on", "brightness": 80},
                    {"device_id": "main_thermostat", "action": "set_temperature", "temperature": 72}
                ],
                enabled=True,
                priority=1
            ),
            ContextualRule(
                id="bedtime_routine",
                name="Bedtime Automation",
                trigger_conditions={
                    "time": "22:00",
                    "occupancy": True
                },
                actions=[
                    {"device_id": "living_room_light", "action": "turn_off"},
                    {"device_id": "kitchen_light", "action": "turn_off"},
                    {"device_id": "bedroom_light", "action": "turn_on", "brightness": 30},
                    {"device_id": "main_thermostat", "action": "set_temperature", "temperature": 68}
                ],
                enabled=True,
                priority=2
            ),
            ContextualRule(
                id="security_mode",
                name="Away Security Mode",
                trigger_conditions={
                    "occupancy": False,
                    "duration_away": 30  # minutes
                },
                actions=[
                    {"device_id": "living_room_light", "action": "turn_off"},
                    {"device_id": "bedroom_light", "action": "turn_off"},
                    {"device_id": "kitchen_light", "action": "turn_off"},
                    {"device_id": "front_door_camera", "action": "enable_recording"},
                    {"device_id": "back_door_camera", "action": "enable_recording"},
                    {"device_id": "main_thermostat", "action": "set_temperature", "temperature": 65}
                ],
                enabled=True,
                priority=3
            ),
            ContextualRule(
                id="morning_routine",
                name="Good Morning Automation",
                trigger_conditions={
                    "time": "07:00",
                    "occupancy": True
                },
                actions=[
                    {"device_id": "living_room_light", "action": "turn_on", "brightness": 90, "temperature": 4000},
                    {"device_id": "kitchen_light", "action": "turn_on", "brightness": 100},
                    {"device_id": "main_thermostat", "action": "set_temperature", "temperature": 73}
                ],
                enabled=True,
                priority=1
            )
        ]
        
        for rule in default_rules:
            self.contextual_rules[rule.id] = rule
    
    def list_devices(self, device_type: Optional[str] = None, location: Optional[str] = None) -> List[Dict]:
        """List all devices with optional filtering"""
        filtered_devices = []
        for device in self.devices.values():
            if device_type and device.type.value != device_type:
                continue
            if location and device.location != location:
                continue
            filtered_devices.append(asdict(device))
        return filtered_devices
    
    def get_device(self, device_id: str) -> Optional[Device]:
        """Get device by ID"""
        return self.devices.get(device_id)
    
    def control_light(self, device_id: str, action: str, **kwargs) -> Dict[str, Any]:
        """Control light device"""
        device = self.get_device(device_id)
        if not device or device.type != DeviceType.LIGHT:
            return {"success": False, "error": "Light device not found"}
        
        if action == "turn_on":
            device.status = DeviceStatus.ON
            device.properties["brightness"] = kwargs.get("brightness", 100)
            if "color" in kwargs:
                device.properties["color"] = kwargs["color"]
            if "temperature" in kwargs:
                device.properties["temperature"] = kwargs["temperature"]
        elif action == "turn_off":
            device.status = DeviceStatus.OFF
            device.properties["brightness"] = 0
        elif action == "set_brightness":
            if device.status == DeviceStatus.ON:
                device.properties["brightness"] = kwargs.get("brightness", 50)
        
        device.last_updated = datetime.now()
        return {"success": True, "message": f"{device.name} {action} completed", "device": asdict(device)}
    
    def control_thermostat(self, device_id: str, action: str, **kwargs) -> Dict[str, Any]:
        """Control thermostat device"""
        device = self.get_device(device_id)
        if not device or device.type != DeviceType.THERMOSTAT:
            return {"success": False, "error": "Thermostat device not found"}
        
        if action == "set_temperature":
            device.properties["target_temp"] = kwargs.get("temperature", 72)
        elif action == "set_mode":
            device.properties["mode"] = kwargs.get("mode", "auto")
        
        device.last_updated = datetime.now()
        return {"success": True, "message": f"Thermostat {action} completed", "device": asdict(device)}
    
    def control_camera(self, device_id: str, action: str, **kwargs) -> Dict[str, Any]:
        """Control security camera"""
        device = self.get_device(device_id)
        if not device or device.type != DeviceType.SECURITY_CAMERA:
            return {"success": False, "error": "Camera device not found"}
        
        if action == "enable_recording":
            device.properties["recording"] = True
        elif action == "disable_recording":
            device.properties["recording"] = False
        elif action == "toggle_motion_detection":
            device.properties["motion_detection"] = not device.properties.get("motion_detection", True)
        
        device.last_updated = datetime.now()
        return {"success": True, "message": f"Camera {action} completed", "device": asdict(device)}
    
    def control_door_lock(self, device_id: str, action: str, **kwargs) -> Dict[str, Any]:
        """Control door lock"""
        device = self.get_device(device_id)
        if not device or device.type != DeviceType.DOOR_LOCK:
            return {"success": False, "error": "Door lock device not found"}
        
        if action == "lock":
            device.status = DeviceStatus.OFF  # OFF = locked
            device.properties["locked"] = True
        elif action == "unlock":
            device.status = DeviceStatus.ON   # ON = unlocked
            device.properties["locked"] = False
        
        device.last_updated = datetime.now()
        return {"success": True, "message": f"Door {action} completed", "device": asdict(device)}
    
    def get_contextual_suggestions(self) -> List[Dict[str, Any]]:
        """Generate contextual suggestions based on current state"""
        suggestions = []
        current_time = datetime.now().time()
        
        # Morning suggestions (6 AM - 9 AM)
        if time(6, 0) <= current_time <= time(9, 0):
            suggestions.append({
                "id": "morning_routine",
                "type": "routine",
                "title": "Good Morning Routine",
                "description": "Turn on lights and adjust temperature for the day",
                "actions": ["turn_on_living_room_light", "set_thermostat_73", "turn_on_kitchen_light"],
                "priority": "high"
            })
        
        # Evening suggestions (6 PM - 10 PM)
        elif time(18, 0) <= current_time <= time(22, 0):
            suggestions.append({
                "id": "evening_routine",
                "type": "routine",
                "title": "Evening Wind Down",
                "description": "Dim lights and prepare for relaxation",
                "actions": ["dim_living_room_light", "set_thermostat_70"],
                "priority": "medium"
            })
        
        # Night suggestions (10 PM - 11 PM)
        elif time(22, 0) <= current_time <= time(23, 0):
            suggestions.append({
                "id": "bedtime_routine",
                "type": "routine",
                "title": "Bedtime Preparation",
                "description": "Activate bedtime routine for better sleep",
                "actions": ["turn_off_main_lights", "dim_bedroom_light", "lower_temperature"],
                "priority": "high"
            })
        
        # Security suggestions when away
        if not any(self.occupancy_status.values()):
            suggestions.append({
                "id": "security_mode",
                "type": "security",
                "title": "Away Mode",
                "description": "Enable security features while away",
                "actions": ["enable_camera_recording", "lock_all_doors", "turn_off_lights"],
                "priority": "high"
            })
        
        # Energy saving suggestions
        active_lights = [d for d in self.devices.values() 
                        if d.type == DeviceType.LIGHT and d.status == DeviceStatus.ON]
        if len(active_lights) > 2:
            suggestions.append({
                "id": "energy_save",
                "type": "energy",
                "title": "Energy Saving",
                "description": "Turn off unused lights to save energy",
                "actions": ["optimize_lighting", "adjust_thermostat"],
                "priority": "low"
            })
        
        return suggestions
    
    def execute_contextual_rule(self, rule_id: str) -> Dict[str, Any]:
        """Execute a contextual automation rule"""
        rule = self.contextual_rules.get(rule_id)
        if not rule or not rule.enabled:
            return {"success": False, "error": "Rule not found or disabled"}
        
        results = []
        for action in rule.actions:
            device_id = action.get("device_id")
            action_type = action.get("action")
            
            # Remove device_id and action from kwargs to avoid duplicate arguments
            action_kwargs = {k: v for k, v in action.items() if k not in ["device_id", "action"]}
            
            device = self.get_device(device_id)
            if not device:
                continue
            
            if device.type == DeviceType.LIGHT:
                result = self.control_light(device_id, action_type, **action_kwargs)
            elif device.type == DeviceType.THERMOSTAT:
                result = self.control_thermostat(device_id, action_type, **action_kwargs)
            elif device.type == DeviceType.SECURITY_CAMERA:
                result = self.control_camera(device_id, action_type, **action_kwargs)
            elif device.type == DeviceType.DOOR_LOCK:
                result = self.control_door_lock(device_id, action_type, **action_kwargs)
            else:
                continue
            
            results.append(result)
        
        return {"success": True, "rule": rule.name, "results": results, "actions_completed": len(results)}
    
    def set_occupancy_status(self, location: str, occupied: bool):
        """Update occupancy status for contextual awareness"""
        self.occupancy_status[location] = occupied
        return {
            "success": True,
            "location": location,
            "occupied": occupied,
            "timestamp": datetime.now().isoformat()
        }
    
    def display_status(self):
        """Display current system status"""
        print("\n" + "="*60)
        print("🏠 SMART HOME STATUS DASHBOARD")
        print("="*60)
        
        # Device status
        print("\n📱 DEVICES:")
        print("-" * 40)
        for device in self.devices.values():
            status_emoji = "🟢" if device.status in [DeviceStatus.ON, DeviceStatus.ACTIVE] else "🔴"
            print(f"{status_emoji} {device.name}")
            print(f"   Location: {device.location}")
            print(f"   Status: {device.status.value}")
            if device.properties:
                key_props = {k: v for k, v in device.properties.items() 
                           if k in ['brightness', 'target_temp', 'recording', 'locked']}
                if key_props:
                    print(f"   Properties: {key_props}")
            print()
        
        # Occupancy status
        print("👥 OCCUPANCY:")
        print("-" * 40)
        if self.occupancy_status:
            for location, occupied in self.occupancy_status.items():
                status = "👤 Occupied" if occupied else "🏠 Empty"
                print(f"{location}: {status}")
        else:
            print("No occupancy data available")
        
        # Contextual suggestions
        suggestions = self.get_contextual_suggestions()
        print(f"\n💡 SUGGESTIONS ({len(suggestions)}):")
        print("-" * 40)
        if suggestions:
            for suggestion in suggestions:
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(suggestion["priority"], "💡")
                print(f"{priority_emoji} {suggestion['title']}")
                print(f"   {suggestion['description']}")
        else:
            print("No suggestions at this time")
        
        print("\n" + "="*60)

async def interactive_demo():
    """Interactive demonstration of the Smart Home Agent"""
    agent = SmartHomeAgent()
    
    print("\n🚀 Welcome to Smart Home Automation Agent Demo!")
    print("Available commands:")
    print("1. status - Show system status")
    print("2. lights <on/off> [room] - Control lights")
    print("3. temp <temperature> - Set thermostat")
    print("4. routine <welcome_home/bedtime_routine/security_mode/morning_routine> - Execute routine")
    print("5. occupy <room> <true/false> - Set occupancy")
    print("6. suggestions - Get contextual suggestions")
    print("7. quit - Exit")
    
    while True:
        try:
            command = input("\n🏠 Smart Home > ").strip().lower()
            
            if command == "quit":
                print("👋 Goodbye!")
                break
            elif command == "status":
                agent.display_status()
            elif command.startswith("lights"):
                parts = command.split()
                if len(parts) >= 2:
                    action = parts[1]
                    room = parts[2] if len(parts) > 2 else "living_room"
                    device_id = f"{room}_light"
                    
                    if action in ["on", "off"]:
                        result = agent.control_light(device_id, f"turn_{action}")
                        if result["success"]:
                            print(f"✅ {result['message']}")
                        else:
                            print(f"❌ {result['error']}")
            elif command.startswith("temp"):
                parts = command.split()
                if len(parts) >= 2:
                    try:
                        temp = int(parts[1])
                        result = agent.control_thermostat("main_thermostat", "set_temperature", temperature=temp)
                        if result["success"]:
                            print(f"✅ {result['message']}")
                        else:
                            print(f"❌ {result['error']}")
                    except ValueError:
                        print("❌ Please provide a valid temperature number")
            elif command.startswith("routine"):
                parts = command.split()
                if len(parts) >= 2:
                    routine_name = parts[1]
                    result = agent.execute_contextual_rule(routine_name)
                    if result["success"]:
                        print(f"✅ Executed '{result['rule']}' routine")
                        print(f"   Completed {result['actions_completed']} actions")
                    else:
                        print(f"❌ {result['error']}")
            elif command.startswith("occupy"):
                parts = command.split()
                if len(parts) >= 3:
                    room = parts[1]
                    occupied = parts[2].lower() == "true"
                    result = agent.set_occupancy_status(room, occupied)
                    status = "occupied" if occupied else "empty"
                    print(f"✅ Set {room} as {status}")
            elif command == "suggestions":
                suggestions = agent.get_contextual_suggestions()
                print(f"\n💡 Contextual Suggestions ({len(suggestions)}):")
                for i, suggestion in enumerate(suggestions, 1):
                    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(suggestion["priority"], "💡")
                    print(f"{i}. {priority_emoji} {suggestion['title']}")
                    print(f"   {suggestion['description']}")
            else:
                print("❌ Unknown command. Type 'quit' to exit.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main entry point"""
    print("🏠 Smart Home Automation Agent with Contextual Awareness")
    print("=" * 60)
    
    # Run interactive demo
    asyncio.run(interactive_demo())

if __name__ == "__main__":
    main()