# <img src="https://github.com/rpetty9/artist_collaboration_project/blob/main/music_icon.png" alt="Music Icon" width="80"/> Artist Collaboration Network

Explore interactive, network-style visualizations of artist collaborations based on predicted streaming and revenue data. This tool helps music professionals analyze trends and identify high-potential partnership opportunities.

---

## 📆 Table of Contents

- [📁 Project Structure](#-project-structure)
- [⚙️ Requirements](#-requirements)
- [🚀 How to Run](#-how-to-run)
- [📊 Viewing the Visualization](#-viewing-the-visualization)
- [🐛 Common Issues & Fixes](#-common-issues--fixes)
- [💡 Performance Tips](#-performance-tips)

---

## 📁 Project Structure

```
├── TODO         # Will update later

```

---

## ⚙️ Requirements

Make sure you have Python 3.8 or higher.

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.gatech.edu/thackler3/dva-project.git
cd dva-project
```

### 2. TODO Add CSV file to github

### 3. Run the Visualization Script

```bash
python graph_network_artist_collaboration_v2.py
```

This creates `artist_collaborations.html` in the current folder.

---

## 📊 Viewing the Visualization

Open the file in your browser:

```bash
xdg-open artist_collaborations.html
```

Or manually open it via your file browser.

### 🌟 Current Features (TODO: Features May change):

- Node sizes based on **revenue**
- Interactive **collaboration filtering**
- **Market-based** filtering (e.g. US, JP, BR)
- Highlight **interconnected artist networks**
- Reset view with the <img src="https://github.gatech.edu/thackler3/dva-project/blob/master/music_icon.png" alt="Music Icon" width="20"/> icon (located top left)

---

## 🐛 Common Issues & Fixes

### ❌ `FileNotFoundError: artist_collaboration_predictions_updated.csv`

**Fix:** Ensure the data file called artist_collaboration_predictions_updated.csv is a ".csv" file format. And make sure to verify the file path in `graph_network_artist_collaboration_v2.py` is correct.

---

### ❌ `ImportError: Missing optional dependency 'openpyxl'`

**Fix:**

```bash
pip install openpyxl
```

---

## 💡 Performance Tips

Rendering large graphs can be demanding on system resources.

📌 **To improve performance:**

- Close unnecessary tabs or background apps

---


*Data Visualization & Analytics* course CSE6242OAN,O01

