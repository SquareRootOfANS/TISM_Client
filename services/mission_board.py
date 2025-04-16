from datetime import datetime

class Mission:
    def __init__(self, title, mission_type, priority, location, description):
        self.title = title
        self.type = mission_type
        self.priority = priority
        self.location = location
        self.description = description
        self.status = "Active"
        self.created_at = datetime.now()

class MissionBoard:
    def __init__(self):
        self.missions = []

    def add_mission(self, mission):
        self.missions.append(mission)

    def get_active_missions(self):
        return [m for m in self.missions if m.status != "Completed"]

    def mark_completed(self, index):
        if 0 <= index < len(self.missions):
            self.missions[index].status = "Completed"
