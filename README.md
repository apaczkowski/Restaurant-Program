# Restaurant Program – Product & Deals Database (Flask App)

A full-stack web application that allows users to filter, analyze, and generate custom reports on restaurant product deals. Built using **Python (Flask)** with an SQLite 
database and a clean UI for interaction.

---

## 🚀 Features

- 🔍 Custom filters for products and deals
- 💰 Dynamic savings analysis (price difference, savings ratio)
- 📄 Report generation via HTML templates
- 🧩 SQLite-based local data storage
- 📐 Basic layout with future Angular integration started

---

## 🛠️ Tech Stack

- **Languages**: Python, JavaScript, HTML/CSS
- **Frameworks/Tools**: Flask, SQLite, Git
- **In Progress**: Angular (in `restaurant-deals/` directory)

---

## 📁 Project Structure
```
Restaurant-Program/
├── Templates/
│ └── report_deal.html # Jinja2 HTML template
├── restaurant-deals/ # Angular placeholder (under development)
├── Restaurant.py # Main Flask application
├── products_and_deals.db # SQLite database
└── README.md
```
## ⚙️ Setup Instructions

##  Clone the repository
    git clone https://github.com/apaczkowski/Restaurant-Program.git
    cd Restaurant-Program

##  Set up a Python environment
    python -m venv venv
    source venv/bin/activate        # On Windows: venv\Scripts\activate
    pip install flask

##  Run the Flask app
    python Restaurant.py
    
##  Open your browser to:
    http://127.0.0.1:5000/

📌 Future Enhancements
-  Deploy app online (Render, Heroku, etc.)
-  Build full Angular frontend (restaurant-deals/)
-  Add authentication (login system)
-  Export reports as PDF/CSV
-  Mobile-friendly layout and CSS polishing

🧠 What I Learned
-  Through this project, I gained hands-on experience in:
-  Building full-stack apps with Flask
-  Structuring Jinja2 templates
-  Handling local databases with SQLite
-  Starting integration with Angular for modern frontend frameworks
-  Project management using Git/GitHub
```
🧑‍💻 Author
   Adam Paczkowski
📍 St. Louis, MO
   https://github.com/apaczkowski
   https://www.linkedin.com/in/adam-paczkowski-b841602b7/
```
