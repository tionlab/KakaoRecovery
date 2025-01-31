import os
from pathlib import Path
import time
import shutil
import filetype
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, PhotoImage
from playsound import playsound 
import webbrowser

def resource_path(relative_path):
    base_path = Path(__file__).parent
    return base_path / relative_path

class KakaoTalkFileRecoveryApp:
    def __init__(self, root):
        self.root = root
        self.stopped = False
        self.setup_ui()

    def setup_ui(self):
        self.root.title("KakaoRecovery")
        self.root.resizable(True, True)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = screen_width // 3
        window_height = screen_height // 3
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.minsize(800, 500)

        icon_path = resource_path('kakao.png')
        icon = PhotoImage(file=icon_path)
        self.root.iconphoto(False, icon)

        menubar = ttk.Menu(self.root)
        self.root.config(menu=menubar)
        menubar.add_cascade(label="사용법", command=self.show_usage)
        menubar.add_cascade(label="License", command=self.show_license)
        self.center_window(self.root) 


        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        title_label = ttk.Label(
            main_frame, 
            text="카카오톡 파일 복구 프로그램", 
            font=("TkDefaultFont", 16, "bold")
        )
        title_label.pack(pady=10)

        input_frame = ttk.LabelFrame(main_frame, text="위치 설정", padding="10")
        input_frame.pack(fill=X, pady=10)

        input_container = ttk.Frame(input_frame)
        input_container.pack(fill=X, pady=5)
        ttk.Label(input_container, text="원본 contents 폴더:").pack(side=LEFT, padx=(0,10))
        self.input_entry = ttk.Entry(input_container)
        self.input_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0,10))
        self.create_btn(input_container, "찾아보기", 
            lambda: self.input_entry.insert(0, filedialog.askdirectory())).pack(side=RIGHT)

        output_container = ttk.Frame(input_frame)
        output_container.pack(fill=X, pady=5)
        ttk.Label(output_container, text="결과물 폴더 (빈 폴더):").pack(side=LEFT, padx=(0,10))
        self.output_entry = ttk.Entry(output_container)
        self.output_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0,10))
        self.create_btn(output_container, "찾아보기", 
            lambda: self.output_entry.insert(0, filedialog.askdirectory())).pack(side=RIGHT)
        
        self.output_placeholder = "./result"
        self.output_entry.insert(0, self.output_placeholder)
        self.output_entry.config(foreground='grey')
        
        self.output_entry.bind("<FocusIn>", self.on_output_entry_focus_in)
        self.output_entry.bind("<FocusOut>", self.on_output_entry_focus_out)

        progress_frame = ttk.LabelFrame(main_frame, text="진행 상태", padding="10")
        progress_frame.pack(fill=X, pady=10)

        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            length=400, 
            mode='determinate',
            style='primary.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill=X, pady=(0,5))

        self.progress_label = ttk.Label(
            progress_frame, 
            text="0.00% (0/0)",
            font=("TkDefaultFont", 10)
        )
        self.progress_label.pack()

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=(0, 20))
        
        inner_button_frame = ttk.Frame(button_frame)
        inner_button_frame.pack(expand=True) 

        self.start_button = self.create_btn(inner_button_frame, "시작", self.start_recovery, 'success')
        self.start_button.pack(side=LEFT, padx=10)

        self.stop_button = self.create_btn(inner_button_frame, "중지", self.stop_recovery, 'danger')
        self.stop_button.pack(side=LEFT, padx=10)
        
        warning_text = " " * 50 + "※ 본 프로그램은 상업적 이용이 금지된 소프트웨어입니다. 최근 본 프로그램의 상업적 사용 사례가 지속적으로 확인되고 있으며, 이는 명백한 라이선스 위반 행위에 해당합니다. 이러한 위반이 계속될 경우, 관련 법률에 따라 법적 대응이 이루어질 수 있음을 엄중히 경고드립니다. ※"
        warning_frame = ttk.Frame(self.root, style='dark.TFrame')
        warning_frame.pack(fill=X, pady=(0, 10))
        
        warning_label = ttk.Label(
            warning_frame,
            text=warning_text,
            font=("TkDefaultFont", 10),
            foreground="red",
            background="black",
            style='dark.TLabel'
        )
        warning_label.pack(pady=5)
        self.scroll_text(warning_label)

    def show_usage(self):
        webbrowser.open("https://www.youtube.com/watch?v=m23KHWat6u8")

    def show_license(self):
        webbrowser.open("https://github.com/tionlab/KakaoRecovery/blob/main/LICENSE")
    
    def scroll_text(self, label):
        text = label.cget("text")
        text = text[1:] + text[0]
        label.config(text=text)
        label.after(100, lambda: self.scroll_text(label))

    def recover_files(self, input_dir, output_dir):
        try:
            total_files = sum(len(files) for _, _, files in os.walk(input_dir))
            self.progress_bar['maximum'] = total_files
            self.progress_bar['value'] = 0
            completed_files = 0 
            for root_dir, _, files in os.walk(input_dir):
                for file_name in files:
                    if self.stopped:
                        break 
                    full_file_path = os.path.join(root_dir, file_name)
                    date_path = time.strftime("/%Y.%m.%d", time.localtime(os.path.getmtime(full_file_path)))
                    file_type = filetype.guess(full_file_path)
                    extension = file_type.extension if file_type else 'unknown'
                    destination_dir = os.path.join(output_dir, date_path.strip('/'))
                    os.makedirs(destination_dir, exist_ok=True)
                    shutil.copy(full_file_path, os.path.join(destination_dir, f"{file_name}.{extension}"))
                    self.progress_bar['value'] += 1
                    completed_files += 1
                    percentage = (completed_files / total_files) * 100
                    self.progress_label.config(text=f"{percentage:.2f}% ({completed_files}/{total_files})")
                    self.root.update()
            if not self.stopped:
                messagebox.showinfo("완료", "복구가 완료되었습니다.")
                playsound(resource_path('end.mp3'))
            self.stopped = False 
        finally:
            self.start_button.config(state='normal')
            self.root.update()
    
    def start_recovery(self):
        input_dir = self.input_entry.get()
        output_dir = self.output_entry.get()
        if not input_dir:
            messagebox.showerror("오류", "원본 폴더를 지정해주세요.")
            return
        if not output_dir or output_dir == self.output_placeholder:
            output_dir = "./result"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        self.start_button.config(state='disabled')
        self.stopped = False
        
        thread = threading.Thread(
            target=self.recover_files,
            args=(input_dir, output_dir),
            daemon=True
        )
        thread.start()
    
    def stop_recovery(self):
        self.stopped = True
    
    def create_btn(self, parent, text, command, style='primary'):
        return ttk.Button(parent, text=text, command=command, style=f'{style}.TButton')
    
    def center_window(self, window):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def on_output_entry_focus_in(self, _):
        if self.output_entry.get() == self.output_placeholder:
            self.output_entry.delete(0, 'end')
            self.output_entry.config(foreground='black')

    def on_output_entry_focus_out(self, _):
        if not self.output_entry.get():
            self.output_entry.insert(0, self.output_placeholder)
            self.output_entry.config(foreground='grey')

def main():
    root = ttk.Window(themename="flatly")
    KakaoTalkFileRecoveryApp(root) 
    root.mainloop()

if __name__ == "__main__":
    main()

# * nuitka --standalone --enable-plugin=tk-inter --mingw64 --windows-console-mode=disable --windows-icon-from-ico=kakao.ico --output-filename=KakaoRecovery.exe --include-data-files=kakao.png=./ --include-data-files=end.mp3=./ gui.py