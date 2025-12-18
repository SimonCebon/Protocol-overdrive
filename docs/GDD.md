# Game Design Document: "Protocol Overdrive" (Final Revision)

## 1. Project Overview

*   **Concept**: A top-down arena survival roguelite. The player controls a survivor facing infinite enemy waves, accumulating "Charge" to unleash abilities or transform into a powerful Robot.
*   **Platform**: PC (Local execution).
*   **Scope**: Single-level MVP (Minimum Viable Product) with an endless loop.

## 2. Technical Configuration

*   **Language**: Python 3.11+
*   **Framework**: pygame-ce (pip install pygame-ce)
*   **Data Storage**: JSON (for local leaderboard persistence).
*   **Display**: 1280x720 (720p), locked at 60 FPS.
*   **Input**:
    *   **Mouse**: Movement (Left Click).
    *   **Keyboard**: Abilities (Q, W, E, R) and Transformation (T).

## 3. Architecture & File Structure

```
/project_root
├── main.py              # Entry point, Game Loop, State Management
├── settings.py          # Constants (SCREEN_WIDTH, SPEEDS, CHARGE_CAP=8)
├── managers.py          # SpawnManager, ScoreManager, CooldownManager
├── sprites.py           # Classes: Player, Enemy, Projectile
├── abilities.py         # Independent Cooldown logic, Skill effects
└── data/
    └── leaderboard.json
```

## 4. Core Mechanics Implementation

### A. Player Controller

*   **Movement (Click-to-Move)**: Mouse Click stores target_vector; Player moves towards it in update().
*   **Auto-Pistol**: Fires automatically at the nearest enemy.
*   **Charge Generation**: Damage conversion logic applies here. charge_gained = damage_dealt * modifier. Higher damage hits yield more charge bits.

### B. The "Charge" & Transformation System

*   **Charge Structure**:
    *   **Data Type**: float. One full charge = 1.0.
    *   **Cap**: Maximum 8.0 full charges.
    *   **Accumulation**: Fractional accumulation (e.g., pistol hit adds 0.20).
    *   **Persistence**: The current_charge value is shared and preserved perfectly when swapping between Human and Robot forms.
*   **State Machine**:
    *   **State.HUMAN**: Uses standard HP. Can spend integer amounts of charges to cast Q, W, E.
    *   **Transformation Trigger**:
        *   **Condition**: Requires current_charge == MAX (8.0).
        *   **Input**: The transformation is not automatic. The player must explicitly press the Transformation Key (T) to initiate the change.
    *   **State.ROBOT**:
        *   **Robot Health (Armor)**: Upon transformation, the player gains a secondary, smaller health bar.
        *   **Revert Condition**: The Robot form does not drain charge over time. Instead, damage taken reduces the Robot Health. When Robot Health reaches 0, the player immediately reverts to State.HUMAN (preserving remaining Charge).

### C. Combat & Abilities

*   **Cooldown System**:
    *   Every ability (Q, W, E, R) has an independent last_cast_time variable.
    *   **Logic**: if current_time - last_cast_time > ability_cooldown: cast_allowed = True.
    *   Usage of one ability does not affect the cooldown of others.
*   **Skill Logic**:
    *   **Normal (Q, W, E)**: Cost 1 or more full charges. Enhanced versions in Robot mode.
    *   **Overdrive (R)**: Unlocked only in Robot mode. Costs significant charge and has a long independent cooldown.

### D. Horde Logic

*   **Spawn Logic**: Enemies spawn outside camera view.
*   **Enemy Types**:
    *   **Standard**: Normal speed and health.
    *   **Fast**: moving faster but with reduced health.
*   **Progression**: Wave N increases enemy count and stats.
*   **Wave Logic**:
    *   **Clearance**: A new wave does not start until all enemies from the current wave are defeated.
    *   **Grace Period**: 3-second pause between waves to allow the player to recover.

## 5. UI & Data Management

*   **HUD**:
    *   **Health Display**: Shows "Base HP" bar. If Robot, overlays a smaller "Armor" bar.
    *   **Charge Meter**: Visualized as 8 distinct slots. Fills fractionally based on the float value.
    *   **Ability Icons**: Visual overlay (grayed out) when on_cooldown is True.
*   **Game Over**: Input nickname, save to leaderboard.json, display Top 10.
    *   **Skip Option**: The player can choose to restart without submitting a score.

## 6. Art & Visual Style Pointers

*   **Style**: Primitive Cyberpunk.
*   **Visual Feedback**:
    *   **Robot Form**: Distinct Sprite change (e.g., Blue Square to Silver Mecha).
    *   **Damage Numbers**: Pop-up text showing damage and charge gained (e.g., "10 dmg (+0.2 chg)").

## 7. MVP Development Roadmap

*   **Setup**: Pygame window and Loop.
*   **Movement & Enemies**: Click-to-move and basic chasers.
*   **Shooting & Charge**: Implement float-based charge accumulation from damage.
*   **UI**: Draw Health (Human) and Charge (8-segment bar).
*   **Abilities**: Implement Q/W/E with independent cooldown timers.
*   **Transformation**: Implement Robot State with manual 'T' key trigger, separate "Armor HP", and Revert logic.
*   **Loop**: Wave manager and Leaderboard.
