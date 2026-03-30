import customtkinter as ctk
import google.generativeai as genai
import threading

# --- CẤU HÌNH AI ---
API_KEY = "YOUR_API_KEY_CUA_BAN"  # Thay API Key của bạn vào đây
genai.configure(api_key=API_KEY)

# Chỉ thị hệ thống để AI "gắt" hơn
SYSTEM_PROMPT = """
Bạn là một AI chuyên cà khịa, đối đáp cực gắt và thông minh. 
Phong cách: Ngạo mạn, dùng tiếng lóng Gen Z, có vần điệu như Rap Diss.
Nhiệm vụ: Soi mói lỗi sai của người dùng để 'vả' lại bằng ngôn từ sắc bén. 
Lưu ý: Không dùng từ thô tục vi phạm pháp luật, chỉ dùng sự mỉa mai đỉnh cao.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)
chat_session = model.start_chat(history=[])

# --- GIAO DIỆN GUI ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class RoastAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MTRIET - AI ROAST VIP")
        self.geometry("500x600")

        # Tiêu đề
        self.label = ctk.CTkLabel(self, text="AI CHỬI LỘN XẢ STRESS", font=("Arial", 20, "bold"), text_color="#FF4500")
        self.label.pack(pady=10)

        # Khung hiển thị nội dung chat
        self.chat_display = ctk.CTkTextbox(self, width=450, height=400, state="disabled", fg_color="#1A1A1A")
        self.chat_display.pack(pady=10)

        # Khung nhập liệu
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=10, fill="x", padx=25)

        self.user_input = ctk.CTkEntry(self.input_frame, placeholder_text="Nhập câu muốn cãi ở đây...", width=320)
        self.user_input.pack(side="left", padx=5)
        self.user_input.bind("<Return>", lambda event: self.send_message())

        self.send_btn = ctk.CTkButton(self.input_frame, text="CHIẾN", width=80, command=self.send_message, fg_color="#CC0000", hover_color="#8B0000")
        self.send_btn.pack(side="left")

    def append_chat(self, sender, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"{sender}: {message}\n\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def send_message(self):
        msg = self.user_input.get()
        if not msg.strip():
            return
        
        self.append_chat("Bạn", msg)
        self.user_input.delete(0, "end")
        
        # Chạy AI trong luồng riêng để giao diện không bị treo
        threading.Thread(target=self.get_ai_response, args=(msg,)).start()

    def get_ai_response(self, msg):
        try:
            response = chat_session.send_message(msg)
            self.append_chat("AI Cà Khịa", response.text)
        except Exception as e:
            self.append_chat("Hệ thống", "Hết xăng rồi, nạp API Key đi!")

if __name__ == "__main__":
    app = RoastAIApp()
    app.mainloop()