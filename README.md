# 👟 FootFit Analyzer — Biomechanics Footwear Profiler

**FootFit Analyzer** is an interactive **Streamlit web app** that uses biomechanics principles and personal characteristics to recommend the best **footwear type** and **material** for each individual.  
It also provides a **visual, step-by-step experience**, from entering your details to receiving an animated recommendation with justifications and comfort metrics.

---

## 🌍 **Live App**
Once deployed, your Streamlit Cloud link will appear here:  
🔗 https://yourusername-biomechanics-footwear-profiler.streamlit.app

---

## 🧠 **About the Project**
This project combines **biomechanical analysis** with an AI-style rule system to analyze:
- Age  
- Gender  
- Weight range  
- Foot type (Flat, Normal, High Arch)  
- Daily activity level  
- Preferred footwear type  

It then recommends:
- The most suitable **shoe category**
- The **best material composition** (with explanation)
- A **comfort meter** rating
- A **foot health tip of the day**

---

## 🎨 **Unique UI Features**
| # | Feature | Description |
|---|----------|--------------|
| 1 | 🎛️ **Sliders for Inputs** | Age, gender, weight, and activity are selected via interactive sliders. |
| 2 | 👣 **Foot Type Visualization** | Displays Flat, Normal, and High Arch icons; highlights the chosen type. |
| 3 | 📊 **Biomechanics Summary Card** | Results shown in a colored, emoji-enhanced summary card. |
| 4 | 🎨 **Dynamic Color Themes** | Background color adapts to activity level: calm blue → light green → energetic orange/red. |
| 5 | 🧍 **Animated Silhouette** | Shows a walking/running GIF when analyzing gait. |
| 6 | 🧵 **Footwear & Material Recommender** | Recommends shoe name, **bold material**, and *italic justification*. |
| 7 | 💡 **Tip of the Day** | Displays random foot health advice. |
| 8 | 👟 **Virtual Shoe Wall** | Shows sample shoe images matching the recommendation. |
| 9 | 🧭 **Step-by-Step Wizard** | Guides users through three screens: Personal Info → Foot Details → Recommendation. |
|10 | 🔊 **Voice Assistant** | Reads the recommendation aloud using browser Text-to-Speech. |
|11 | 🎯 **Custom Banner / Logo** | Displays “FootFit Analyzer” branding or your logo. |

---

## 🦶 **Biomechanics Logic Overview**
| Factor | Rule Applied | Example Outcome |
|---------|---------------|----------------|
| **Foot Type** | Determines arch support and cushioning needs | Flat → High support; High Arch → Extra cushioning |
| **Weight** | Adjusts cushioning level | Over 90 kg → High cushioning |
| **Activity Level** | Sets background and shoe type | High → Running shoes |
| **Footwear Preference** | Personalized override | User preference shown alongside recommended type |
| **Material Rule System** | Suggests ideal shoe material with justification | EVA, mesh, or foam combinations based on needs |

---

## 🗂️ **Project Structure**
