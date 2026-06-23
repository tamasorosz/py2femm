import customtkinter as ctk
import threading
from attempts.pacek_dataclass import MotorParameters, run_bldc_analysis # Ügyelj rá, hogy a mappa útvonala helyes legyen!

# Modern kinézet beállítása
ctk.set_appearance_mode("System")  # Követi a Windows sötét/világos módját
ctk.set_default_color_theme("blue")

class BldcApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BLDC Motor Tervező - FEMM Szimuláció")
        self.geometry("400x350")

        # Címsor
        self.label_title = ctk.CTkLabel(self, text="BLDC Paraméterek", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(pady=(20, 10))

        # --- Horonyszám bemenet ---
        self.frame_slots = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_slots.pack(pady=5)
        self.label_slots = ctk.CTkLabel(self.frame_slots, text="Stator Hornyok Száma:", width=150, anchor="w")
        self.label_slots.pack(side="left", padx=10)
        self.entry_slots = ctk.CTkEntry(self.frame_slots, width=100)
        self.entry_slots.insert(0, "24") # Alapérték
        self.entry_slots.pack(side="left")

        # --- Légrés bemenet ---
        self.frame_gap = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_gap.pack(pady=5)
        self.label_gap = ctk.CTkLabel(self.frame_gap, text="Légrés mérete (mm):", width=150, anchor="w")
        self.label_gap.pack(side="left", padx=10)
        self.entry_gap = ctk.CTkEntry(self.frame_gap, width=100)
        self.entry_gap.insert(0, "0.7") # Alapérték
        self.entry_gap.pack(side="left")

        # --- Szimuláció Gomb ---
        self.btn_run = ctk.CTkButton(self, text="Szimuláció Indítása", command=self.start_simulation)
        self.btn_run.pack(pady=(30, 10))

        # --- Státusz kijelző ---
        self.label_status = ctk.CTkLabel(self, text="Várakozás...", text_color="gray")
        self.label_status.pack(pady=5)

    def start_simulation(self):
        """Külön szálon indítja a szimulációt, hogy ne fagyjon le a GUI ablak."""
        self.btn_run.configure(state="disabled")
        self.label_status.configure(text="Szimuláció fut... Kérlek várj!", text_color="orange")
        
        # Egy külön szálon (Thread) futtatjuk, különben a Windows "Not responding" hibát adna
        threading.Thread(target=self.run_femm_logic, daemon=True).start()

    def run_femm_logic(self):
        try:
            # 1. Beolvassuk a GUI-ból az értékeket
            motor = MotorParameters()
            motor.stator_slots = int(self.entry_slots.get())
            motor.air_gap_length = float(self.entry_gap.get())

            # 2. Lefuttatjuk a te kódodat
            run_bldc_analysis(motor_params=motor)

            # 3. Frissítjük a GUI-t siker esetén
            self.label_status.configure(text="Sikeres szimuláció! Fájlok generálva.", text_color="green")
        except Exception as e:
            # Hiba esetén kiírjuk a GUI-ra
            self.label_status.configure(text=f"Hiba: {str(e)}", text_color="red")
        finally:
            self.btn_run.configure(state="normal")

if __name__ == "__main__":
    app = BldcApp()
    app.mainloop()