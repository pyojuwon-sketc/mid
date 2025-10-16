import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox

def on_focus_in(event):
    """텍스트 영역에 포커스가 들어왔을 때 플레이스홀더를 제거합니다."""
    widget = event.widget
    if widget.get(1.0, "end-1c") == placeholder_text:
        widget.delete(1.0, tk.END)
        widget.config(foreground=default_fg_color)

def on_focus_out(event):
    """텍스트 영역에서 포커스가 나갔을 때 내용이 없으면 플레이스홀더를 추가합니다."""
    widget = event.widget
    if not widget.get(1.0, "end-1c"):
        widget.insert(1.0, placeholder_text, "center")
        widget.config(foreground="grey")

if __name__ == "__main__":
    # 1. 메인 윈도우(창) 생성
    main_window = tk.Tk()

    # 2. 창의 제목 설정
    main_window.title("메모장")

    # 3. 창의 크기 설정
    main_window.geometry("800x600")

    # 4. 텍스트 입력 영역 추가
    text_area = scrolledtext.ScrolledText(main_window, wrap=tk.WORD, undo=True)
    text_area.pack(expand=True, fill='both')

    # 5. 플레이스홀더(안내 문구) 기능 구현
    placeholder_text = "메모장을 만들어봐요"
    
    # 가운데 정렬을 위한 태그 설정
    text_area.tag_configure("center", justify='center')

    # 기본 글자색 저장 및 이벤트 바인딩
    default_fg_color = text_area.cget("foreground")
    text_area.bind("<FocusIn>", on_focus_in)
    text_area.bind("<FocusOut>", on_focus_out)

    # 초기 플레이스홀더 설정 (FocusOut 이벤트 강제 호출)
    text_area.event_generate("<<FocusOut>>")

    # 6. 윈도우가 화면에 계속 나타나도록 처리
    main_window.mainloop()
