import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import os

class NotepadApp:
    """
    간단한 메모장 애플리케이션 클래스
    """
    def __init__(self, root):
        self.root = root
        self.root.title("제목 없음 - 메모장")
        self.root.geometry("800x600")

        # 현재 열려있는 파일 경로를 저장하기 위한 변수
        self.current_file_path = None

        # 플레이스홀더 텍스트 설정
        self.placeholder_text = "메모장을 만들어봐요"

        # 텍스트 입력 영역 생성 (스크롤 기능 포함)
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, undo=True)
        self.text_area.pack(expand=True, fill='both')

        # 플레이스홀더 텍스트를 가운데 정렬하기 위한 태그 설정
        self.text_area.tag_configure("center", justify='center')

        # 플레이스홀더 기능 구현
        self.default_fg_color = self.text_area.cget("foreground")
        self.text_area.bind("<FocusIn>", self.on_focus_in)
        self.text_area.bind("<FocusOut>", self.on_focus_out)
        
        # 초기 플레이스홀더 설정
        self.on_focus_out(None)

        # 메뉴 바 생성
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # 파일 메뉴 생성
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="파일(F)", menu=file_menu)
        file_menu.add_command(label="새로 만들기(N)", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="열기(O)...", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="저장(S)", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="다른 이름으로 저장(A)...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="끝내기(X)", command=self.exit_app)

        # 편집 메뉴 생성
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="편집(E)", menu=edit_menu)
        edit_menu.add_command(label="실행 취소(U)", accelerator="Ctrl+Z", command=self.undo)
        edit_menu.add_command(label="다시 실행(R)", accelerator="Ctrl+Y", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="잘라내기(T)", accelerator="Ctrl+X", command=self.cut)
        edit_menu.add_command(label="복사(C)", accelerator="Ctrl+C", command=self.copy)
        edit_menu.add_command(label="붙여넣기(P)", accelerator="Ctrl+V", command=self.paste)
        edit_menu.add_command(label="삭제(L)", accelerator="Del", command=self.delete)
        edit_menu.add_separator()
        edit_menu.add_command(label="모두 선택(A)", accelerator="Ctrl+A", command=self.select_all)

        # 단축키 바인딩
        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        # Ctrl+A, Ctrl+Y 등은 ScrolledText 위젯이 자체적으로 처리하는 경우가 많지만,
        # 메뉴와의 일관성을 위해 명시적으로 바인딩할 수 있습니다.
        self.root.bind("<Control-a>", lambda event: self.select_all())
        self.root.bind("<Control-y>", lambda event: self.redo())
        
        # 창을 닫을 때 확인 절차
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def on_focus_in(self, event):
        """텍스트 영역에 포커스가 들어왔을 때 플레이스홀더를 제거합니다."""
        if self.text_area.get(1.0, "end-1c") == self.placeholder_text:
            self.text_area.delete(1.0, tk.END)
            self.text_area.config(foreground=self.default_fg_color)

    def on_focus_out(self, event):
        """텍스트 영역에서 포커스가 나갔을 때 내용이 없으면 플레이스홀더를 추가합니다."""
        if not self.text_area.get(1.0, "end-1c"):
            self.text_area.insert(1.0, self.placeholder_text, "center")
            self.text_area.config(foreground="grey")

    def get_content(self):
        """실제 내용을 반환합니다. 플레이스홀더는 빈 문자열로 처리합니다."""
        content = self.text_area.get(1.0, "end-1c")
        if content == self.placeholder_text:
            return ""
        return self.text_area.get(1.0, tk.END)

    def new_file(self):
        """새 파일을 만듭니다."""
        if self.get_content().strip():
            if not messagebox.askyesno("경고", "저장하지 않은 변경사항이 있습니다. 계속하시겠습니까?"):
                return
        self.text_area.delete(1.0, tk.END)
        self.current_file_path = None
        self.root.title("제목 없음 - 메모장")
        self.on_focus_out(None)

    def open_file(self):
        """파일을 엽니다."""
        if self.get_content().strip():
            if not messagebox.askyesno("경고", "저장하지 않은 변경사항이 있습니다. 계속하시겠습니까?"):
                return
        file_path = filedialog.askopenfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding='utf-8') as file:
                    self.on_focus_in(None)
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.INSERT, file.read())
                self.current_file_path = file_path
                self.root.title(f"{os.path.basename(file_path)} - 메모장")
            except Exception as e:
                messagebox.showerror("오류", f"파일을 여는 중 오류가 발생했습니다: {e}")

    def save_file(self):
        """현재 파일을 저장합니다. 새 파일인 경우 다른 이름으로 저장을 호출합니다."""
        if self.current_file_path:
            try:
                content = self.get_content()
                with open(self.current_file_path, "w", encoding='utf-8') as file:
                    file.write(content)
                self.root.title(f"{os.path.basename(self.current_file_path)} - 메모장")
            except Exception as e:
                messagebox.showerror("오류", f"파일을 저장하는 중 오류가 발생했습니다: {e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        """파일을 다른 이름으로 저장합니다."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.current_file_path = file_path
            self.save_file()

    def exit_app(self):
        """애플리케이션을 종료합니다."""
        if self.get_content().strip():
            response = messagebox.askyesnocancel("메모장", f"'{self.root.title()}'의 내용을 저장하시겠습니까?")
            if response is True: # '예'를 선택한 경우
                self.save_file()
                # save_file에서 사용자가 취소할 수도 있으므로, 파일이 실제로 저장되었는지 확인
                if self.current_file_path:
                    self.root.destroy()
            elif response is False: # '아니오'를 선택한 경우
                self.root.destroy()
            else: # '취소' 또는 창 닫기
                return
        else:
            self.root.destroy()

    # --- 편집 기능 메서드 ---

    def undo(self, event=None):
        """실행을 취소합니다."""
        self.text_area.edit_undo()
        return "break"

    def redo(self, event=None):
        """다시 실행합니다."""
        self.text_area.edit_redo()
        return "break"

    def cut(self, event=None):
        """선택한 텍스트를 잘라냅니다."""
        self.text_area.event_generate("<<Cut>>")
        return "break"

    def copy(self, event=None):
        """선택한 텍스트를 복사합니다."""
        self.text_area.event_generate("<<Copy>>")
        return "break"

    def paste(self, event=None):
        """텍스트를 붙여넣습니다."""
        self.text_area.event_generate("<<Paste>>")
        return "break"

    def delete(self, event=None):
        """선택한 텍스트를 삭제합니다."""
        self.text_area.event_generate("<<Clear>>")
        return "break"

    def select_all(self, event=None):
        """모든 텍스트를 선택합니다."""
        self.text_area.event_generate("<<SelectAll>>")
        return "break"

if __name__ == "__main__":
    # 1. 메인 윈도우(창) 생성
    main_window = tk.Tk()
    app = NotepadApp(main_window)
    main_window.mainloop()
