# smart_unit_converter_gui.py
# Smart Unit Converter (GUI) - Tkinter
# Features: dropdown category + conversion, input validation, result display

import tkinter as tk
from tkinter import ttk, messagebox


# --- Conversion functions ---
def kg_to_lb(x): return x * 2.2046226218
def lb_to_kg(x): return x / 2.2046226218

def c_to_f(x): return (x * 9 / 5) + 32
def f_to_c(x): return (x - 32) * 5 / 9
def c_to_k(x): return x + 273.15
def k_to_c(x): return x - 273.15

def km_to_miles(x): return x * 0.6213711922
def miles_to_km(x): return x / 0.6213711922
def m_to_ft(x): return x * 3.280839895
def ft_to_m(x): return x / 3.280839895

def s_to_min(x): return x / 60
def min_to_s(x): return x * 60
def min_to_h(x): return x / 60
def h_to_min(x): return x * 60


CONVERSIONS = {
    "Weight": {
        "kg → lb": (kg_to_lb, "lb"),
        "lb → kg": (lb_to_kg, "kg"),
    },
    "Temperature": {
        "°C → °F": (c_to_f, "°F"),
        "°F → °C": (f_to_c, "°C"),
        "°C → K":  (c_to_k, "K"),
        "K → °C":  (k_to_c, "°C"),
    },
    "Distance": {
        "km → miles": (km_to_miles, "miles"),
        "miles → km": (miles_to_km, "km"),
        "m → ft":     (m_to_ft, "ft"),
        "ft → m":     (ft_to_m, "m"),
    },
    "Time": {
        "seconds → minutes": (s_to_min, "min"),
        "minutes → seconds": (min_to_s, "s"),
        "minutes → hours":   (min_to_h, "h"),
        "hours → minutes":   (h_to_min, "min"),
    }
}


def safe_float(s: str) -> float:
    s = s.strip().replace(",", ".")
    if not s:
        raise ValueError("Empty input.")
    return float(s)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Unit Converter")
        self.geometry("520x280")
        self.resizable(False, False)

        # --- Title ---
        title = ttk.Label(self, text="Smart Unit Converter", font=("Segoe UI", 16, "bold"))
        title.pack(pady=(14, 4))

        subtitle = ttk.Label(self, text="Choose a category, conversion type, and enter a value.")
        subtitle.pack(pady=(0, 10))

        # --- Main frame ---
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="both", expand=True)

        # Category
        ttk.Label(frame, text="Category:").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        self.category_var = tk.StringVar(value="Weight")
        self.category_cb = ttk.Combobox(
            frame, textvariable=self.category_var, state="readonly", width=28,
            values=list(CONVERSIONS.keys())
        )
        self.category_cb.grid(row=0, column=1, sticky="w", pady=6)
        self.category_cb.bind("<<ComboboxSelected>>", self.on_category_change)

        # Conversion
        ttk.Label(frame, text="Conversion:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        self.conv_var = tk.StringVar()
        self.conv_cb = ttk.Combobox(frame, textvariable=self.conv_var, state="readonly", width=28)
        self.conv_cb.grid(row=1, column=1, sticky="w", pady=6)

        # Input value
        ttk.Label(frame, text="Value:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
        self.value_var = tk.StringVar()
        self.value_entry = ttk.Entry(frame, textvariable=self.value_var, width=31)
        self.value_entry.grid(row=2, column=1, sticky="w", pady=6)
        self.value_entry.insert(0, "0")

        # Buttons
        btns = ttk.Frame(frame)
        btns.grid(row=3, column=1, sticky="w", pady=(10, 6))

        self.convert_btn = ttk.Button(btns, text="Convert", command=self.convert)
        self.convert_btn.grid(row=0, column=0, padx=(0, 8))

        self.clear_btn = ttk.Button(btns, text="Clear", command=self.clear)
        self.clear_btn.grid(row=0, column=1)

        # Result
        ttk.Label(frame, text="Result:").grid(row=4, column=0, sticky="nw", padx=(0, 8), pady=(10, 0))
        self.result_var = tk.StringVar(value="—")
        self.result_label = ttk.Label(frame, textvariable=self.result_var, font=("Segoe UI", 12))
        self.result_label.grid(row=4, column=1, sticky="w", pady=(10, 0))

        # Status tip
        self.tip_var = tk.StringVar(value="Tip: You can use decimals, e.g. 12.5 or 12,5")
        tip = ttk.Label(self, textvariable=self.tip_var)
        tip.pack(pady=(0, 10))

        # Initialize conversion list
        self.on_category_change()
        self.value_entry.focus_set()

        # Enter triggers convert
        self.bind("<Return>", lambda _e: self.convert())

    def on_category_change(self, *_):
        cat = self.category_var.get()
        options = list(CONVERSIONS[cat].keys())
        self.conv_cb["values"] = options
        self.conv_var.set(options[0])
        self.result_var.set("—")

    def validate_domain(self, category: str, conversion: str, value: float) -> None:
        # Domain checks to avoid nonsense
        if category == "Time" and value < 0:
            raise ValueError("Time values cannot be negative.")
        if category == "Temperature" and conversion.startswith("K") and value < 0:
            raise ValueError("Kelvin cannot be negative.")

    def convert(self):
        cat = self.category_var.get()
        conv = self.conv_var.get()

        try:
            value = safe_float(self.value_var.get())
            self.validate_domain(cat, conv, value)

            func, unit = CONVERSIONS[cat][conv]
            out = func(value)

            # formatting
            if cat == "Temperature":
                formatted = f"{out:.2f} {unit}"
            else:
                formatted = f"{out:.4f} {unit}"

            self.result_var.set(formatted)

        except KeyError:
            messagebox.showerror("Error", "Please select a valid conversion.")
        except ValueError as e:
            messagebox.showwarning("Invalid input", str(e))
        except Exception:
            messagebox.showerror("Error", "Something went wrong. Please try again.")

    def clear(self):
        self.value_var.set("")
        self.result_var.set("—")
        self.value_entry.focus_set()


if __name__ == "__main__":
    # Use ttk theme for a cleaner look
    app = App()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass

    app.mainloop()
