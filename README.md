# ⚔️ Clash of Clans Farming Bot 🤖

An **intelligent automation bot** for Clash of Clans that automatically searches for resource-rich bases and farms them using **OCR** and **computer vision**.

---

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green?logo=open-source-initiative)
![Status](https://img.shields.io/badge/Status-Active-success)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

---

## ⚡ Features

* 🤖 **Intelligent Base Search** — Uses OCR to find loot-rich bases automatically
* ⚔️ **Automated Attacking** — Deploys troops autonomously in an optimized pattern
* ⚙️ **Configurable Thresholds** — Set custom gold/elixir/dark minimums
* 📈 **Progress Tracking** — Tracks loot gained, attacks, and total performance
* 🧩 **Easy Setup** — Interactive coordinate setup system
* 💾 **Persistent Config** — Saves settings in `cache.json` for reuse

---

## 🎯 How It Works

1. 🔍 **Base Search** — Scans bases and reads loot via **EasyOCR**
2. ⚖️ **Evaluation** — Compares loot with your set thresholds
3. 🪖 **Attack** — Deploys troops in a 4-line pattern
4. 💰 **Loot Collection** — Reads earned resources from results screen
5. 🔁 **Repeat** — Returns to lobby and starts the next cycle

---

## 🔧 Installation

### Prerequisites

* 🐍 Python 3.8+
* 💻 Windows, macOS, or Linux
* 📱 Clash of Clans running in **windowed** or **emulator** mode

### Install Dependencies

```bash
pip install pillow pyautogui easyocr opencv-python numpy
```

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/coc-farming-bot.git
cd coc-farming-bot
```

---

## 🚀 Quick Start

### 🧭 First-Time Setup

1. **Run Setup**

   ```bash
   python main.py --setup
   ```

2. **Select Configuration**

   * Option 1: Resource regions (6 clicks)
   * Option 2: Result screen regions (6 clicks)
   * Option 3: Action buttons (7 clicks)
   * Option 4: Deployment zones (8 clicks)
   * Option 5: Everything (27 clicks)

3. **Start Farming**

   ```bash
   python main.py
   ```

### 🔄 Normal Usage

Once setup is done:

```bash
python main.py
```

The bot will auto-load your configuration from `cache.json`.

---

## ⚙️ Configuration

### Default Farm Targets (around line 560)

```python
farm_loop(
    target_gold=14000000,  # Stop after farming 14M gold
    target_elixir=14000000,  # Stop after farming 14M elixir
    target_dark=500  # Stop after farming 500 dark
)
```

### Loot Thresholds (around line 547)

```python
gold_threshold = 500000   # Minimum gold to attack
elixir_threshold = 500000 # Minimum elixir to attack
dark_threshold = 50000    # Minimum dark elixir to attack
```

---

## 📁 Project Structure

```
coc-farming-bot/
├── main.py            # Main bot script
├── cache.json         # Saved coordinates (auto-generated)
├── README.md          # This file
├── LICENSE            # MIT License
└── requirements.txt   # Python dependencies
```

---

## 🎮 Usage Examples

### Example 1: Farm Until 10M Gold/Elixir

```python
farm_loop(
    target_gold=10000000,
    target_elixir=10000000,
    target_dark=50000
)
```

### Example 2: Reconfigure Only Buttons

```bash
python main.py --setup
```

---

## 📊 Statistics Tracking

Real-time dashboard includes:

* 🧮 Current attack number
* 💰 Total loot gained (gold/elixir/dark)
* 📊 Progress percentage
* ⏱️ Time elapsed

---

## ⚠️ Important Notes

### 🧠 Educational Purposes Only

This bot demonstrates:

* OCR and computer vision
* Screen automation
* State machine architecture
* Python scripting

### 🚨 Use at Your Own Risk

* May violate **Clash of Clans Terms of Service**
* Use on **secondary accounts only**
* Not responsible for bans

### ✅ Recommendations

* Avoid 24/7 runtime (simulate human behavior)
* Periodically monitor
* Use moderate attack frequency

---

## 🛠️ Troubleshooting

### OCR Not Reading Correctly

* Ensure window is in focus
* Match screen resolution
* Re-run `--setup`
* Increase OCR delay

### Bot Clicking Wrong Spots

* Reconfigure via `python main.py --setup`
* Ensure emulator window isn’t moved

### Bot Stuck or Frozen

* Check terminal logs
* Verify coordinates
* Ensure stable connection

---

## 🔄 Updating Coordinates

If window size/resolution changes:

```bash
python main.py --setup
```

Choose:

* `[5]` for full reconfiguration
* `[1–4]` for partial updates

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch

   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit changes

   ```bash
   git commit -m "Add amazing feature"
   ```
4. Push and open a Pull Request

---

## 🧠 Technical Details

**Technologies Used**

* 🖼️ PIL (Pillow) — Screen capture
* 🎮 PyAutoGUI — Input automation
* 🔍 EasyOCR — Text detection
* 📸 OpenCV — Image processing
* 🔢 NumPy — Numerical operations

**Architecture**

* State-machine based design
* Coordinate-based automation
* OCR + JSON config system
* Modular attack logic

---

## 🧭 Flow Diagram

```
┌──────────────────┐
│   Start Bot      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Search for Base  │◄────────────┐
└────────┬─────────┘             │
         ▼                       │
┌──────────────────┐             │
│  Read Resources  │             │
│     (OCR)        │             │
└────────┬─────────┘             │
         ▼                       │
┌──────────────┐                 │
│  Good Loot?  │─────────────────┘
└───┬────┬─────┘
    │    │
   No   Yes
    │    ▼
    │ ┌────────────┐
    │ │Deploy Troops│
    │ └────┬────────┘
    │      ▼
    │ ┌────────────┐
    │ │ Wait End   │
    │ └────┬────────┘
    │      ▼
    │ ┌────────────┐
    │ │ Read Loot  │
    │ └────┬────────┘
    │      ▼
    │ ┌────────────┐
    │ │Return Lobby│
    │ └────────────┘
```

---

## 📜 License

This project is licensed under the **MIT License**.
See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

* Built as a **learning project** in automation engineering
* Inspired by computer vision and OCR exploration
* Thanks to the open-source Python community 💙

---

## 📧 Contact

Have suggestions or issues?
👉 [Open an issue on GitHub](#)

---

> ⚠️ **Disclaimer**: This bot is for **educational purposes only**.
> The developers are **not responsible** for any account bans or violations of ToS.
>
> 🎮 **Happy Farming — Responsibly!**
