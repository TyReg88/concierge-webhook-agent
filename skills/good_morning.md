---
name: good_morning
description: Activates the Good Morning scene, opening all window covers/blinds in the house.
---

# Good Morning Skill

## Goal
The goal of this skill is to transition the house to day-time mode by opening all simulated window covers (blinds/roller shutters) across all floors.

## Constraints & Usage Guidelines
* **Trigger Conditions**: Use this skill when the user greets with "Good morning" (or "Guten Morgen" / "Morgen"), indicates they are waking up or starting the day, or explicitly asks to open all window covers/roller shutters.
* **Scope**: This action operates globally on all devices in the house belonging to the `cover` domain.
* **Reference**: The execution is handled by the script [scripts/good_morning.py](../scripts/good_morning.py).
