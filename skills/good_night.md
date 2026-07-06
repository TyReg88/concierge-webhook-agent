---
name: good_night
description: Activates the Good Night scene, closing all window covers/blinds in the house.
---

# Good Night Skill

## Goal
The goal of this skill is to transition the house to night-time mode by closing all simulated window covers (blinds/roller shutters) across all floors.

## Constraints & Usage Guidelines
* **Trigger Conditions**: Use this skill when the user greets with "Good night" (or "Gute Nacht" / "Nacht"), indicates they are going to bed/sleep, or explicitly asks to close all window covers/roller shutters.
* **Scope**: This action operates globally on all devices in the house belonging to the `cover` domain.
* **Reference**: The execution is handled by the script [scripts/good_night.py](../scripts/good_night.py).
