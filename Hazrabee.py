#importing modules
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

import tkinter as tk

# checking eligibility function
def check_eligibility():
    report_text.delete("1.0", tk.END) # deleting the data

    loan_type = loan_type_var.get()
    try:
        age = int(age_entry.get())
        income = int(income_entry.get())
        credit = int(credit_entry.get())
        loan_amount = int(loan_amount_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Enter valid numbers for Age, Income, Credit Score, and Loan Amount.")
        return

    employment = employment_var.get()
    extra = extra_entry.get().strip()

    eligible = False
    reasons = []

   # if age <= 0 or income < 0 or credit < 0 or loan_amount <= 0:
       # messagebox.showerror("Input Error", "Age, Income, Credit Score, and Loan Amount must be positive numbers.")
       # return
    if credit < 300 or credit > 900:
        messagebox.showerror("Input Error", "Credit Score must be between 300 and 900.")
        return
    if employment == "":
        employment = "Unemployed"

    if loan_type == "Home Loan":
        try:
            property_value = int(extra)
        except:
            messagebox.showerror("Input Error", "Enter valid Property Value for Home Loan.")
            return
        if age >= 21 and income >= 30000 and credit >= 700 and property_value >= 500000 and loan_amount <= property_value:
            eligible = True
        else:
            reasons.append("Age ≥21, Income ≥₹30K, Credit Score ≥700, Property Value ≥₹5L, Loan ≤ Property Value")

    elif loan_type == "Car Loan":
        if age >= 21 and income >= 30000 and credit >= 700 and loan_amount <= income * 20:
            eligible = True
        else:
            reasons.append("Age ≥21, Income ≥₹30K, Credit Score ≥700, Loan ≤ 20x Income")

    elif loan_type == "Education Loan":
        valid_courses = ["engineering", "medical", "mba", "law", "science", "arts"]
        if age >= 17 and credit >= 700 and extra.lower() in valid_courses and loan_amount <= 2000000:
            eligible = True
        else:
            reasons.append(f"Age ≥21, Credit Score ≥600, Course in {', '.join(valid_courses)}, Loan ≤ ₹20L")

    elif loan_type == "Personal Loan":
        if age >= 21 and income >= 30000 and credit >= 700 and employment != "Unemployed" and loan_amount <= income * 15:
            eligible = True
        else:
            reasons.append("Age ≥21, Income ≥₹30K, Credit ≥700, Employed, Loan ≤ 15x Income")

    elif loan_type == "Business Loan":
        if age >= 21 and income >= 50000 and credit >= 720 and employment != "Unemployed" and loan_amount <= income * 25:
            eligible = True
        else:
            reasons.append("Age ≥21, Income ≥₹50K, Credit ≥700, Employed, Loan ≤ 25x Income")

    elif loan_type == "Gold Loan":
        try:
            gold_value = int(extra)
        except:
            messagebox.showerror("Input Error", "Enter valid Gold Value for Gold Loan.")
            return
        if age >= 21 and credit >= 7000 and gold_value >= loan_amount:
            eligible = True
        else:
            reasons.append("Age ≥21, Credit ≥700, Gold Value ≥ Loan Amount")

    else:
        messagebox.showerror("Loan Type", "Please select a valid loan type.")
        return

    emi_text = ""
    if eligible:
        try:
            tenure = int(tenure_entry.get())
            rate = float(interest_entry.get())
            if tenure <= 0 or rate <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Enter valid positive numbers for Tenure and Interest Rate.")
            return

        r = rate / (12 * 100)
        n = tenure * 12
        emi = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)
        emi_text = f"Estimated EMI: ₹{emi:,.2f} for {tenure} years at {rate}% interest.\n"
    else:
        emi_text = "EMI calculation skipped due to ineligibility.\n"

    report = f"Loan Type: {loan_type}\nAge: {age}\nIncome: ₹{income}\nCredit Score: {credit}\nEmployment: {employment}\nLoan Amount: ₹{loan_amount}\n"
    if loan_type == "Home Loan":
        report += f"Property Value: ₹{extra}\n"
    elif loan_type == "Education Loan":
        report += f"Course: {extra}\n"
    elif loan_type == "Gold Loan":
        report += f"Gold Value: ₹{extra}\n"
    report += "\n"

    if eligible:
        report += "✅ You are eligible for this loan.\n"
    else:
        report += "❌ You are NOT eligible for this loan.\n"
        report += "Reasons:\n" + "\n".join(f"- {r}" for r in reasons) + "\n"

    report += "\n" + emi_text
    report_text.insert(tk.END, report)

def update_extra_label(event):
    loan = loan_type_var.get()
    extra_entry.delete(0, tk.END)
    if loan == "Home Loan":
        extra_label.config(text="Property Value (₹):")
        extra_entry.config(state="normal")
    elif loan == "Education Loan":
        extra_label.config(text="Course Name:")
        extra_entry.config(state="normal")
    elif loan == "Gold Loan":
        extra_label.config(text="Gold Value (₹):")
        extra_entry.config(state="normal")
    else:
        extra_label.config(text="(Not Required)")
        extra_entry.delete(0, tk.END)
        extra_entry.config(state="disabled")

def save_report():
    content = report_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Save Error", "No report to save. Please check eligibility first.")
        return
    try:
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"loan_eligibility_report_{now}.txt"
        with open(filename, "w",encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Report saved as {filename}")
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save report:\n{e}")

def reset_fields():
    loan_type_var.set('')
    age_entry.delete(0, tk.END)
    income_entry.delete(0, tk.END)
    credit_entry.delete(0, tk.END)
    employment_var.set('')
    extra_entry.config(state="normal")
    extra_entry.delete(0, tk.END)
    loan_amount_entry.delete(0, tk.END)
    tenure_entry.delete(0, tk.END)
    interest_entry.delete(0, tk.END)
    report_text.delete("1.0", tk.END)
    extra_label.config(text="(Not Required)")

# GUI SETUP
root = tk.Tk()
root.title("Loan Eligibility Checker")
root.geometry("1000x600")
root.configure(bg="lightpink")

title = tk.Label(root, text="💰 Loan Eligibility Checker", font=("Helvetica", 20, "bold"),
                 fg="black", bg="orange", pady=10)
title.pack(fill="x")

# --- Main Frame ---
main_frame = tk.Frame(root, bg="#FFE4B5")
main_frame.pack(fill="both", expand=True)

# --- Left Frame (Input) ---
input_frame = tk.Frame(main_frame, bg="#FFF8DC", padx=20, pady=20)
input_frame.grid(row=0, column=0, sticky="nsew")

def create_label(text):
    return tk.Label(input_frame, text=text, bg="#FFF8DC", font=("Helvetica", 11, "bold"))

create_label("Select Loan Type:").pack(anchor="w")
loan_type_var = tk.StringVar()
loan_type_combo = ttk.Combobox(input_frame, textvariable=loan_type_var, state="readonly")
loan_type_combo['values'] = ("Home Loan", "Car Loan", "Education Loan", "Personal Loan", "Business Loan", "Gold Loan")
loan_type_combo.pack(fill="x", pady=5)
loan_type_combo.bind("<<ComboboxSelected>>", update_extra_label)

create_label("Enter Age:").pack(anchor="w")
age_entry = tk.Entry(input_frame)
age_entry.pack(fill="x", pady=5)

create_label("Monthly Income (₹):").pack(anchor="w")
income_entry = tk.Entry(input_frame)
income_entry.pack(fill="x", pady=5)

create_label("Credit Score (300-900):").pack(anchor="w")
credit_entry = tk.Entry(input_frame)
credit_entry.pack(fill="x", pady=5)

create_label("Employment Type:").pack(anchor="w")
employment_var = tk.StringVar()
employment_combo = ttk.Combobox(input_frame, textvariable=employment_var, state="readonly")
employment_combo['values'] = ("Salaried", "Self-Employed", "Unemployed")
employment_combo.pack(fill="x", pady=5)

extra_label = create_label("(Not Required)")
extra_label.pack(anchor="w")
extra_entry = tk.Entry(input_frame)
extra_entry.pack(fill="x", pady=5)

create_label("Loan Amount (₹):").pack(anchor="w")
loan_amount_entry = tk.Entry(input_frame)
loan_amount_entry.pack(fill="x", pady=5)

create_label("Loan Tenure (Years):").pack(anchor="w")
tenure_entry = tk.Entry(input_frame)
tenure_entry.pack(fill="x", pady=5)

create_label("Interest Rate (% per annum):").pack(anchor="w")
interest_entry = tk.Entry(input_frame)
interest_entry.pack(fill="x", pady=5)

tk.Button(input_frame, text="Check Eligibility", command=check_eligibility,
          bg="green", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10, fill="x")

tk.Button(input_frame, text="Save Report", command=save_report,
          bg="blue", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5, fill="x")

tk.Button(input_frame, text="Reset", command=reset_fields,
          bg="red", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5, fill="x")

# --- Right Frame (Output) ---
output_frame = tk.Frame(main_frame, bg="#FFF8DC", padx=20, pady=20)
output_frame.grid(row=0, column=1, sticky="nsew")

tk.Label(output_frame, text="📋 Eligibility Report", font=("Helvetica", 14, "bold"),
         bg="#FFF8DC").pack(anchor="w", pady=5)

report_text = tk.Text(output_frame, height=30, width=50, bg="white",fg="purple", font=("Consolas", 11))
report_text.pack(fill="both", expand=True)

# Grid configuration
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

root.mainloop()


# applications
''' 1. easy documentation
    2. attractive interest rate
    3. easy processing
    4.Conveninence
    5.instant approval'''