import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
from models.player import Player
from models.coach import Coach

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def main_gui(team):
    root = ctk.CTk()
    root.title("Basketball Team Manager")
    
    # ✅ Fullscreen & ESC to Exit
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

    root.configure(fg_color="#0b1e45")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # KIRI
    left_frame = ctk.CTkFrame(root, fg_color="transparent")
    left_frame.grid(row=0, column=0, sticky="nsew", padx=(50, 20), pady=40)

    # Judul diperbesar
    ctk.CTkLabel(left_frame, text="🏀 My Basketball Team", font=("Poppins", 50, "bold"), text_color="white").pack(anchor="w", pady=(30, 10))
    ctk.CTkLabel(left_frame, text="Manage your basketball team with ease", font=("Poppins", 22), text_color="#d6d6d6").pack(anchor="w", pady=(0, 60))

    button_grid = ctk.CTkFrame(left_frame, fg_color="transparent")
    button_grid.pack()

    def create_button(text, icon, command):
        return ctk.CTkButton(
            master=button_grid,
            text=f"{icon}  {text}",
            font=("Poppins", 16, "bold"),
            text_color="white",
            fg_color="#1f3b7a",
            hover_color="#2e57b5",
            width=200,
            height=60,
            corner_radius=12,
            command=command
        )

    def create_input_popup(title, fields, on_submit, initial_values=None):
        popup = ctk.CTkToplevel(root)
        popup.title(title)
        popup.geometry("400x420")
        popup.configure(fg_color="#1a1a3a")
        popup.grab_set()

        entries = {}
        ctk.CTkLabel(popup, text=title, font=("Poppins", 18, "bold"), text_color="white").pack(pady=15)
        form_frame = ctk.CTkFrame(popup, fg_color="transparent")
        form_frame.pack(pady=10)

        for field in fields:
            ctk.CTkLabel(form_frame, text=field, font=("Poppins", 12), text_color="white").pack(anchor="w", pady=(10, 0))
            if field == "Position":
                combo = ctk.CTkOptionMenu(form_frame, values=["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"], width=280)
                if initial_values:
                    combo.set(initial_values.get(field, ""))
                combo.pack()
                entries[field] = combo
            else:
                entry = ctk.CTkEntry(form_frame, width=280)
                if initial_values:
                    entry.insert(0, str(initial_values.get(field, "")))
                entry.pack()
                entries[field] = entry

        def submit():
            try:
                values = [entries[field].get().strip() for field in fields]
                if all(values):
                    on_submit(*values)
                    popup.destroy()
                else:
                    messagebox.showwarning("Input Error", "Please fill out all fields.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(popup, text="Submit", command=submit, fg_color="#3a87d4", hover_color="#4b9ef2").pack(pady=20)

    def add_player():
        def handle_add(name, age, number, position):
            player = Player(name, int(age), int(number), position)
            team.add_player(player)
            team.save_to_file()
            messagebox.showinfo("Player Added", f"{name.title()}, #{number} - {position.title()}, {age} yrs old")
        create_input_popup("Add Player", ["Name", "Age", "Jersey Number", "Position"], handle_add)

    def add_coach():
        if team.coach:
            messagebox.showwarning("Coach Exists", "A coach has already been assigned.")
            return
        def handle_add(name, age, experience):
            coach = Coach(name, int(age), int(experience))
            team.set_coach(coach)
            team.save_to_file()
            messagebox.showinfo("Coach Added", f"{name.title()}, {age} yrs, {experience} yrs experience")
        create_input_popup("Add Coach", ["Name", "Age", "Experience (years)"], handle_add)

    def show_team():
        popup = ctk.CTkToplevel(root)
        popup.title("Team Info")
        popup.geometry("700x600")
        popup.configure(fg_color="#121229")
        popup.grab_set()

        ctk.CTkLabel(popup, text=f"🏀 {team.name} Roster", font=("Poppins", 24, "bold"), text_color="white").pack(pady=20)

        coach_frame = ctk.CTkFrame(popup, fg_color="#1f1f3a", corner_radius=10)
        coach_frame.pack(fill="x", padx=30, pady=10)
        ctk.CTkLabel(coach_frame, text="👨‍🏫 Coach", font=("Poppins", 16, "bold"), text_color="white").pack(anchor="w", padx=15, pady=(10, 0))

        if team.coach:
            ctk.CTkLabel(coach_frame, text=team.coach.show_info(), font=("Poppins", 14), text_color="white").pack(anchor="w", padx=15, pady=10)
            btn_row = ctk.CTkFrame(coach_frame, fg_color="transparent")
            btn_row.pack(pady=(0, 10))

            def edit_coach():
                initial = {"Name": team.coach.name, "Age": team.coach.age, "Experience (years)": team.coach.experience}
                def handle_edit(name, age, experience):
                    team.set_coach(Coach(name, int(age), int(experience)))
                    team.save_to_file()
                    popup.destroy()
                    show_team()
                create_input_popup("Edit Coach", ["Name", "Age", "Experience (years)"], handle_edit, initial)

            def delete_coach():
                if messagebox.askyesno("Confirm Delete", "Delete this coach?"):
                    team.set_coach(None)
                    team.save_to_file()
                    popup.destroy()
                    show_team()

            ctk.CTkButton(btn_row, text="Edit", command=edit_coach, fg_color="#3a87d4", width=80).pack(side="left", padx=5)
            ctk.CTkButton(btn_row, text="Delete", command=delete_coach, fg_color="#d43f3a", width=80).pack(side="left", padx=5)
        else:
            ctk.CTkLabel(coach_frame, text="No coach assigned.", font=("Poppins", 14), text_color="white").pack(padx=15, pady=10)

        players_frame = ctk.CTkScrollableFrame(popup, width=640, height=350, fg_color="#1a1a3a")
        players_frame.pack(pady=10)

        ctk.CTkLabel(players_frame, text="🧍 Players", font=("Poppins", 16, "bold"), text_color="white").pack(anchor="w", padx=10, pady=(10, 0))

        if team.players:
            for idx, player in enumerate(team.players):
                p_frame = ctk.CTkFrame(players_frame, fg_color="#26264d", corner_radius=8)
                p_frame.pack(fill="x", pady=6, padx=10)

                ctk.CTkLabel(p_frame, text=f"{player.show_info()}", font=("Poppins", 13), text_color="white").pack(anchor="w", padx=10, pady=8)

                btns = ctk.CTkFrame(p_frame, fg_color="transparent")
                btns.pack(pady=5)

                def make_edit_handler(i=idx):
                    def edit():
                        p = team.players[i]
                        initial = {"Name": p.name, "Age": p.age, "Jersey Number": p.number, "Position": p.position}
                        def handle_edit(name, age, number, position):
                            team.players[i] = Player(name, int(age), int(number), position)
                            team.save_to_file()
                            popup.destroy()
                            show_team()
                        create_input_popup("Edit Player", ["Name", "Age", "Jersey Number", "Position"], handle_edit, initial)
                    return edit

                def make_delete_handler(i=idx):
                    def delete():
                        if messagebox.askyesno("Confirm Delete", "Delete this player?"):
                            team.players.pop(i)
                            team.save_to_file()
                            popup.destroy()
                            show_team()
                    return delete

                ctk.CTkButton(btns, text="Edit", command=make_edit_handler(), fg_color="#3a87d4", width=80).pack(side="left", padx=5)
                ctk.CTkButton(btns, text="Delete", command=make_delete_handler(), fg_color="#d43f3a", width=80).pack(side="left", padx=5)
        else:
            ctk.CTkLabel(players_frame, text="No players added yet.", font=("Poppins", 13), text_color="white").pack(pady=20)

    buttons = [
        create_button("Add Player", "➕", add_player),
        create_button("Add Coach", "🎓", add_coach),
        create_button("Show Info", "📋", show_team),
        create_button("Exit", "❌", root.destroy),
    ]

    for i, btn in enumerate(buttons):
        btn.grid(row=i // 2, column=i % 2, padx=20, pady=30)

    # KANAN
    right_frame = ctk.CTkFrame(root, fg_color="transparent")
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 50), pady=40)

    image_path = os.path.join(os.getcwd(), "assets", "basket_player.png")
    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((500, 500))
        ctk_img = ctk.CTkImage(light_image=img, size=(500, 500))
        image_label = ctk.CTkLabel(right_frame, image=ctk_img, text="")
        image_label.pack(expand=True)
    else:
        ctk.CTkLabel(right_frame, text="[Image Not Found]", font=("Poppins", 16), text_color="white").pack(expand=True)

    root.mainloop()
