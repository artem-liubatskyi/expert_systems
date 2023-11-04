import tkinter as tk
from tkinter import ttk, messagebox
from ES.COVID_19 import get_assessment


def assess_risk():
    assessement = get_assessment(
        symptoms=[symptom for symptom in symptoms if symptoms_vars[symptom].get()],
        age=int(age_input.get()),
        underlying_conditions=[condition for condition in underlying_conditions if conditions_vars[condition].get()],
        vaccination_status=vaccination_status_var.get(),
        occupation=occupation_var.get(),
        living_condition=living_condition_var.get(),
        travel_history=travel_history_var.get()
    )
    
    messagebox.showinfo(f"Assessment", f"{assessement}")

app = tk.Tk()
app.title("COVID-19 Risk Assessment Tool")

symptoms = ["fever", "cough", "shortness of breath", "loss of taste", "loss of smell", "fatigue", "muscle aches"]
underlying_conditions = ["diabetes", "chronic lung disease", "heart disease", "chronic kidney disease", "hypertension", "obesity"]
vaccination_statuses = ["vaccinated", "unvaccinated"]
occupations = ["healthcare_worker", "essential_worker", "other"]
living_conditions = ["high_density", "medium_density", "low_density"]

symptoms_vars = {symptom: tk.BooleanVar() for symptom in symptoms}
conditions_vars = {condition: tk.BooleanVar() for condition in underlying_conditions}
vaccination_status_var = tk.StringVar()
occupation_var = tk.StringVar()
living_condition_var = tk.StringVar()
travel_history_var = tk.BooleanVar()

ttk.Label(app, text="Select Symptoms:").pack(anchor="w")
for symptom in symptoms:
    ttk.Checkbutton(app, text=symptom.title(), variable=symptoms_vars[symptom]).pack(anchor="w")

ttk.Label(app, text="Select Underlying Conditions:").pack(anchor="w")
for condition in underlying_conditions:
    ttk.Checkbutton(app, text=condition.title(), variable=conditions_vars[condition]).pack(anchor="w")

ttk.Label(app, text="Select Vaccination Status:").pack(anchor="w")
vaccination_status_dropdown = ttk.Combobox(app, textvariable=vaccination_status_var, values=vaccination_statuses, state="readonly")
vaccination_status_dropdown.pack()

ttk.Label(app, text="Select Occupation:").pack(anchor="w")
occupation_dropdown = ttk.Combobox(app, textvariable=occupation_var, values=occupations, state="readonly")
occupation_dropdown.pack()

ttk.Label(app, text="Select Living Condition:").pack(anchor="w")
living_condition_dropdown = ttk.Combobox(app, textvariable=living_condition_var, values=living_conditions, state="readonly")
living_condition_dropdown.pack()

ttk.Checkbutton(app, text="Travel History", variable=travel_history_var).pack(anchor="w")

def only_numeric_input(value):
    return value.isdigit() or value == ""


ttk.Label(app, text="Age:").pack(anchor="w")
age_input = ttk.Entry(app, validate="key", validatecommand=(app.register(only_numeric_input), '%P'))
age_input.pack()

ttk.Button(app, text="Assess Risk", command=assess_risk).pack()

app.mainloop()