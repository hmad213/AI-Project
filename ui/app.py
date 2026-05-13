import os
import sys
import joblib
import threading
import customtkinter as ctk
from tkinter import StringVar

UI_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(UI_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.tokenizer import clean_text

MODEL_PATH  = os.path.join(ROOT_DIR, "models", "sarcasm_model.pkl")
WINNER_PATH = os.path.join(ROOT_DIR, "models", "winner_name.txt")

try:
    model = joblib.load(MODEL_PATH)
    with open(WINNER_PATH) as f:
        model_name = f.read().strip()
except Exception as e:
    model = None
    model_name = "N/A"
    print(f"[WARN] Could not load model: {e}")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ACCENT = "#00B6EE"
ACCENT2 = "#DB2222" 
ACCENT3 = "#73FC02"
BG_DEEP = "#0D0D0D"
BG_CARD = "#141414"
BG_INPUT = "#1A1A1A"
TEXT_MAIN = "#E8E8E8"
TEXT_DIM = "#555555"
FONT_MONO = ("Courier New", 13)
FONT_BIG = ("Courier New", 28, "bold")
FONT_MED = ("Courier New", 14, "bold")
FONT_SMALL = ("Courier New", 11)

HISTORY_MAX = 50 

def predict(text: str):
    cleaned = clean_text(text)
    pred    = model.predict([cleaned])[0]
    try:
        proba = model.predict_proba([cleaned])[0]
        conf  = f"{max(proba)*100:.1f}%"
    except AttributeError:
        conf = "—"
    return int(pred), conf


class SarcasmApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"Sarcasm Detector")
        self.geometry("820x640")
        self.minsize(640, 520)
        self.configure(fg_color=BG_DEEP)

        self._history: list[tuple[str, int, str]] = [] 
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # ── Header ──
        header = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=1, sticky="w", padx=50, pady=14)

        ctk.CTkLabel(
            title_frame, text=f"SARCASM DETECTOR > {model_name}",
            font=FONT_BIG, text_color=TEXT_MAIN
        ).pack(anchor="w")

        input_card = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        input_card.grid(row=1, column=0, sticky="ew", padx=20, pady=(16, 0))
        input_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            input_card, text="ENTER SENTENCE",
            font=FONT_SMALL, text_color=TEXT_DIM
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 4))

        self.entry_var = StringVar()
        self.entry = ctk.CTkEntry(
            input_card,
            textvariable=self.entry_var,
            placeholder_text="Type something",
            font=FONT_MONO,
            height=46,
            fg_color=BG_INPUT,
            border_color=ACCENT,
            border_width=1,
            text_color=TEXT_MAIN,
        )
        self.entry.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.entry.bind("<Return>", lambda _: self._run_prediction())

        self.analyze_btn = ctk.CTkButton(
            input_card,
            text="ANALYZE  ▶",
            font=FONT_MED,
            height=44,
            fg_color=ACCENT,
            text_color="#000000",
            hover_color="#029ECE",
            corner_radius=6,
            command=self._run_prediction,
        )
        self.analyze_btn.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 16))

        # ── Result Banner ──
        self.result_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        self.result_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=12)
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(1, weight=1)

        # top: verdict area
        verdict_row = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        verdict_row.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 6))
        verdict_row.grid_columnconfigure(1, weight=1)

        self.verdict_icon = ctk.CTkLabel(
            verdict_row, text="●",
            font=("Courier New", 40, "bold"), text_color=TEXT_DIM, width=52
        )
        self.verdict_icon.grid(row=0, column=0, rowspan=2)

        self.verdict_label = ctk.CTkLabel(
            verdict_row, text="Awaiting input…",
            font=("Courier New", 20, "bold"), text_color=TEXT_DIM, anchor="w"
        )
        self.verdict_label.grid(row=0, column=1, sticky="w", padx=10)

        # divider
        div = ctk.CTkFrame(self.result_frame, fg_color=TEXT_DIM, height=1)
        div.grid(row=1, column=0, sticky="ew", padx=16, pady=4)

        # history scroll area
        ctk.CTkLabel(
            self.result_frame, text="HISTORY",
            font=FONT_SMALL, text_color=TEXT_DIM
        ).grid(row=2, column=0, sticky="w", padx=16, pady=(6, 2))

        self.history_box = ctk.CTkScrollableFrame(
            self.result_frame, fg_color="transparent", corner_radius=0
        )
        self.history_box.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.result_frame.grid_rowconfigure(3, weight=1)

    def _run_prediction(self):
        text = self.entry_var.get().strip()

        self.analyze_btn.configure(state="disabled", text="ANALYZING…")
        threading.Thread(target=self._predict_thread, args=(text,), daemon=True).start()

    def _predict_thread(self, text: str):
        try:
            pred, conf = predict(text)
            self.after(0, self._show_result, text, pred, conf)
        except Exception as e:
            self.after(0, self._reset_btn)

    def _show_result(self, text: str, pred: int, conf: str):
        sarcastic = pred == 1
        color  = ACCENT2 if sarcastic else ACCENT3
        icon   = "◈" if sarcastic else "◉"
        label  = "SARCASTIC" if sarcastic else "NOT SARCASTIC"

        self.verdict_icon.configure(text=icon,  text_color=color)
        self.verdict_label.configure(text=label, text_color=color)

        # add history row
        self._history.insert(0, (text, pred, conf))
        if len(self._history) > HISTORY_MAX:
            self._history.pop()
        self._refresh_history()

        self.entry_var.set("")
        self._reset_btn()

    def _refresh_history(self):
        for w in self.history_box.winfo_children():
            w.destroy()

        for i, (txt, pred, conf) in enumerate(self._history):
            sarcastic = pred == 1
            color = ACCENT2 if sarcastic else ACCENT3
            tag   = "SARCASTIC" if sarcastic else "REAL"

            row = ctk.CTkFrame(self.history_box, fg_color=BG_INPUT, corner_radius=6)
            row.pack(fill="x", pady=3, padx=2)
            row.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                row, text=f"[{tag}]",
                font=("Courier New", 11, "bold"), text_color=color, width=60
            ).grid(row=0, column=0, padx=(10, 6), pady=6, sticky="w")

            ctk.CTkLabel(
                row, text=txt,
                font=FONT_SMALL, text_color=TEXT_MAIN, anchor="w", wraplength=540
            ).grid(row=0, column=1, padx=4, pady=6, sticky="w")

            ctk.CTkLabel(
                row, text=conf,
                font=FONT_SMALL, text_color=TEXT_DIM, width=52
            ).grid(row=0, column=2, padx=(4, 10), pady=6, sticky="e")

    def _reset_btn(self):
        self.analyze_btn.configure(state="normal", text="ANALYZE  ▶")
        self.entry.focus_set()


if __name__ == "__main__":
    app = SarcasmApp()
    app.mainloop()