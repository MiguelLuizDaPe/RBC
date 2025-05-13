import tkinter as tk
from tkinter import messagebox
import csv


weights = {
    "Age": 0.7,
    "Gender": 0.2,
    "Avg_BPM": 1,
    "Session_Duration": 0.8,
    "Workout_Type": 1,
    "Fat_Percentage": 0.5,
    "Workout_Frequency": 1,
    "Experience_Level": 0.6,
    "BMI": 0.8,
    "Calories_Burned": 1,
}


age_mapping = {1: "Até 25", 2: "26 até 35", 3: "36 até 45", 4: "46 até 59"}
gender_mapping = {"Male": 1, "Female": 2}
workout_type_mapping = {"Yoga": 1, "Strength": 2, "Cardio": 3, "HIIT": 4}


def map_session_duration(session_duration):
    if session_duration <= 0.60:
        return 1
    elif 0.60 < session_duration <= 0.90:
        return 2
    elif 0.90 < session_duration <= 1.20:
        return 3
    elif 1.20 < session_duration <= 1.40:
        return 4
    else:
        return 5
    
def map_calories_burned(calories_burned):
    if calories_burned <= 200:
        return 1
    elif 200 < calories_burned <= 400:
        return 2
    elif 400 < calories_burned <= 600:
        return 3
    elif 600 < calories_burned <= 700:
        return 4
    elif 700 < calories_burned <= 900:
        return 5
    else:
        return 6

def map_fat_percentage(fat_percentage):
    if fat_percentage <= 10:
        return 1
    elif 10 < fat_percentage <= 20:
        return 2
    elif 20 < fat_percentage <= 30:
        return 3
    elif 30 < fat_percentage <= 40:
        return 4
    else:
        return 5

def map_bmi(bmi):
    if bmi <= 10:
        return 1
    elif 10 < bmi <= 20:
        return 2
    elif 20 < bmi <= 30:
        return 3
    elif 30 < bmi <= 40:
        return 4
    else:
        return 5

def sim_local(input_case, case, max_val, min_val):
    if max_val == min_val:
        return 1 if input_case == case else 0
    return 1 - abs(input_case - case) / (max_val - min_val)

def calcular_similaridades(caso1, caso2, weights):
    sim = 0
    total_weight = 0

    def add_similarity(attribute, max_val, min_val):
        nonlocal sim, total_weight
        weight = weights.get(attribute, 0)
        sim += weight * sim_local(caso1.get(attribute), caso2.get(attribute), max_val, min_val)
        total_weight += weight

    add_similarity("Age", 4, 1)
    add_similarity("Gender", 2, 1)
    add_similarity("Avg_BPM", 5, 1)
    add_similarity("Session_Duration", 5, 1)
    add_similarity("Workout_Type", 4, 1)
    add_similarity("Fat_Percentage", 5, 1)
    add_similarity("Workout_Frequency", 5, 1)
    add_similarity("Experience_Level", 3, 1)
    add_similarity("BMI", 5, 1)
    add_similarity("Calories_Burned", 6, 1)

    if total_weight > 0:
        return sim / total_weight
    else:
        return 0

def rank_cases_by_similarity(input_case, cases):
    similarities = []
    for i, case in enumerate(cases):
        sim = calcular_similaridades(input_case, case, weights)
        similarities.append((i, sim))
    return sorted(similarities, key=lambda x: x[1], reverse=True)

def display_ranked_cases(ranked_cases, cases, input_case):
    result_text.delete(1.0, tk.END) 
    result_text.insert(tk.END, "Ranking dos casos mais similares:\n")
    if ranked_cases:
        first_case_index = ranked_cases[0][0]
        first_case = cases[first_case_index]
        result_text.insert(tk.END, "\nDetalhes do caso mais similar:\n")
        result_text.insert(tk.END, f"Idade: {first_case['Age']}\n")
        result_text.insert(tk.END, f"Gênero: {'Masculino' if first_case['Gender'] == 1 else 'Feminino'}\n")
        result_text.insert(tk.END, f"BPM Médio: {first_case['Avg_BPM']}\n")
        result_text.insert(tk.END, f"Duração da Sessão: {first_case['Session_Duration']}\n")
        result_text.insert(tk.END, f"Tipo de Treino: {first_case['Workout_Type']}\n")
        result_text.insert(tk.END, f"Percentual de Gordura: {first_case['Fat_Percentage']}\n")
        result_text.insert(tk.END, f"Frequência de Treino: {first_case['Workout_Frequency']} dias/semana\n")
        result_text.insert(tk.END, f"Nível de Experiência: {first_case['Experience_Level']}\n")
        result_text.insert(tk.END, f"Índice de Massa Corporal (BMI): {first_case['BMI']}\n")
        result_text.insert(tk.END, f"Calorias Queimadas: {first_case['Calories_Burned']}\n")
        
    for rank, (i, sim) in enumerate(ranked_cases):
        if sim < 0:
            sim = 0
        case_desc = f"Caso {rank} | Similaridade: {sim*100:.2f}%"
        result_text.insert(tk.END, case_desc + "\n")

def load_cases():
    with open("data.csv", newline="") as file:
        reader = csv.DictReader(file)
        cases = []
        for row in reader:
            case = {
                "Age": int(row["Age"]),
                "Gender": gender_mapping[row["Gender"]],
                "Avg_BPM": int(row["Avg_BPM"]),
                "Session_Duration": map_session_duration(float(row["Session_Duration (hours)"])),
                "Workout_Type": workout_type_mapping[row["Workout_Type"]],
                "Fat_Percentage": map_fat_percentage(float(row["Fat_Percentage"])),
                "Workout_Frequency": int(row["Workout_Frequency (days/week)"]),
                "Experience_Level": int(row["Experience_Level"]),
                "BMI": map_bmi(float(row["BMI"])),
                "Calories_Burned": map_calories_burned(float(row["Calories_Burned"])),
            }
            cases.append(case)
    return cases


root = tk.Tk()
root.title("Sistema de Similaridade de Casos")


canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)


canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


weights_entries = {}
for key in weights:
    tk.Label(scrollable_frame, text=f"Peso para {key}:").pack()
    entry = tk.Entry(scrollable_frame)
    entry.insert(0, str(weights[key]))
    entry.pack()
    weights_entries[key] = entry


tk.Label(scrollable_frame, text="Idade do caso de entrada:").pack()
input_age = tk.Entry(scrollable_frame)
input_age.pack()

tk.Label(scrollable_frame, text="Gênero do caso de entrada (1=Male, 2=Female):").pack()
input_gender = tk.Entry(scrollable_frame)
input_gender.pack()

tk.Label(scrollable_frame, text="BPM médio do caso de entrada:").pack()
input_bpm = tk.Entry(scrollable_frame)
input_bpm.pack()

tk.Label(scrollable_frame, text="Duração da sessão (horas):").pack()
input_session_duration = tk.Entry(scrollable_frame)
input_session_duration.pack()

tk.Label(scrollable_frame, text="Tipo de treino (1=Yoga, 2=Strength, 3=Cardio, 4=HIIT):").pack()
input_workout_type = tk.Entry(scrollable_frame)
input_workout_type.pack()

tk.Label(scrollable_frame, text="Percentual de gordura do caso de entrada:").pack()
input_fat_percentage = tk.Entry(scrollable_frame)
input_fat_percentage.pack()

tk.Label(scrollable_frame, text="Frequência de treino (dias por semana):").pack()
input_workout_frequency = tk.Entry(scrollable_frame)
input_workout_frequency.pack()

tk.Label(scrollable_frame, text="Nível de experiência (1=Beginner, 2=Medium, 3=Expert):").pack()
input_experience_level = tk.Entry(scrollable_frame)
input_experience_level.pack()

tk.Label(scrollable_frame, text="Índice de Massa Corporal (BMI):").pack()
input_bmi = tk.Entry(scrollable_frame)
input_bmi.pack()

tk.Label(scrollable_frame, text="Calorias queimadas:").pack()
input_calories_burned = tk.Entry(scrollable_frame)
input_calories_burned.pack()


result_text = tk.Text(scrollable_frame, height=10, width=50)
result_text.pack()

def on_submit():
    
    for key in weights:
        weights[key] = float(weights_entries[key].get())
    
   
    input_case = {
        "Age": int(input_age.get()),
        "Gender": int(input_gender.get()),
        "Avg_BPM": int(input_bpm.get()),
        "Session_Duration": map_session_duration(float(input_session_duration.get())),
        "Workout_Type": int(input_workout_type.get()),
        "Fat_Percentage": map_fat_percentage(float(input_fat_percentage.get())),
        "Workout_Frequency": int(input_workout_frequency.get()),
        "Experience_Level": int(input_experience_level.get()),
        "BMI": map_bmi(float(input_bmi.get())),
        "Calories_Burned": map_calories_burned(float(input_calories_burned.get()))
    }
    
    cases = load_cases()
    ranked_cases = rank_cases_by_similarity(input_case, cases)
    display_ranked_cases(ranked_cases, cases, input_case)

submit_button = tk.Button(scrollable_frame, text="Calcular Similaridade", command=on_submit)
submit_button.pack()

root.mainloop()
