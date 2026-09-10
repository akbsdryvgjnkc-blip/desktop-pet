import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import threading
import random
import os

class DesktopPet:
    def __init__(self, root):
        self.root = root
        self.root.title("桌面电子宠物 - 毛毛")
        
        # 无边框窗口设置
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)  # 总是在最上层
        self.root.geometry("300x300+100+100")  # 宽x高+x坐标+y坐标
        self.root.configure(bg='#f0f0f0')
        
        # 设置透明背景（可选，如果想要透明背景）
        # self.root.attributes('-transparentcolor', '#f0f0f0')
        
        self.video_dir = r"C:\Users\联想\Desktop\bam"
        self.videos = {
            'lick': os.path.join(self.video_dir, '1.mp4'),
            'walk': os.path.join(self.video_dir, '2.mp4'),
            'stare': os.path.join(self.video_dir, '3.mp4'),
            'roll': os.path.join(self.video_dir, '4.mp4'),
            'tired': os.path.join(self.video_dir, '5.mp4'),
        }
        
        self.check_videos()
        self.pet_name = "毛毛"
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.is_playing_video = False
        
        # 拖动窗口的变量
        self.drag_data = {"x": 0, "y": 0}
        
        self.setup_ui()
        self.update_status()
        self.setup_drag()
        
    def check_videos(self):
        missing = []
        for action, path in self.videos.items():
            if not os.path.exists(path):
                missing.append(f"{action}: {path}")
        
        if missing:
            print("⚠️ 视频文件未找到，请检查路径")
    
    def setup_drag(self):
        """设置窗口拖动功能"""
        self.root.bind("<Button-1>", self.on_press)
        self.root.bind("<B1-Motion>", self.on_drag)
    
    def on_press(self, event):
        """鼠标按下时记录位置"""
        self.drag_data["x"] = event.x_root - self.root.winfo_x()
        self.drag_data["y"] = event.y_root - self.root.winfo_y()
    
    def on_drag(self, event):
        """拖动窗口"""
        x = event.x_root - self.drag_data["x"]
        y = event.y_root - self.drag_data["y"]
        self.root.geometry(f"+{x}+{y}")
    
    def setup_ui(self):
        # 只有视频显示区域
        self.video_label = tk.Label(
            self.root,
            bg='#f0f0f0',
            width=40,
            height=15,
            relief=tk.FLAT,
            borderwidth=0,
            text="",
            font=("微软雅黑", 12),
            fg='#999'
        )
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # 右键菜单
        self.create_context_menu()
        
        # 绑定事件
        self.video_label.bind("<Button-3>", self.show_menu)  # 右键
        self.video_label.bind("<Button-2>", self.on_middle_click)  # 中键快速切换动作
    
    def create_context_menu(self):
        """创建右键菜单"""
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="🍖 喂食", command=self.feed)
        self.menu.add_command(label="🎮 玩耍", command=self.play)
        self.menu.add_command(label="👀 逗它", command=self.tease)
        self.menu.add_command(label="😴 休息", command=self.sleep)
        self.menu.add_command(label="❤️ 爱抚", command=self.pet)
        self.menu.add_separator()
        self.menu.add_command(label="📊 显示状态", command=self.show_status)
        self.menu.add_separator()
        self.menu.add_command(label="❌ 退出", command=self.root.quit)
    
    def show_menu(self, event):
        """显示右键菜单"""
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()
    
    def on_middle_click(self, event):
        """中键快速玩耍"""
        self.play()
    
    def update_status(self):
        """每10秒更新一次状态"""
        self.hunger = min(100, self.hunger + 0.8)
        self.happiness = max(0, self.happiness - 0.3)
        self.energy = max(0, self.energy - 0.2)
        
        self.root.after(10000, self.update_status)
    
    def play_video(self, video_name):
        """播放视频"""
        if self.is_playing_video:
            return
        
        if video_name not in self.videos:
            return
        
        video_path = self.videos[video_name]
        
        if not os.path.exists(video_path):
            self.show_emotion(f"❌ 找不到视频")
            return
        
        self.is_playing_video = True
        thread = threading.Thread(target=self._play_video_thread, args=(video_path,), daemon=True)
        thread.start()
    
    def _play_video_thread(self, video_path):
        """在单独线程中播放视频"""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                self.show_emotion("❌ 无法打开视频")
                return
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_delay = max(10, int(1000 / fps)) if fps > 0 else 33
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # 调整帧大小以适应窗口
                frame = cv2.resize(frame, (300, 300))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image)
                
                self.video_label.config(image=photo, text='')
                self.video_label.image = photo
                
                self.root.after(frame_delay)
            
            cap.release()
        except Exception as e:
            print(f"播放视频出错: {str(e)}")
            self.show_emotion(f"❌ 出错")
        finally:
            self.is_playing_video = False
            self.root.after(500, self.show_idle_state)
    
    def show_idle_state(self):
        """显示待机状态"""
        self.video_label.config(bg='#f0f0f0', text="😊", font=("微软雅黑", 80), fg='#ffb6c1')
        self.video_label.image = None
    
    def show_emotion(self, text):
        """显示情绪文本"""
        self.video_label.config(text=text, font=("微软雅黑", 20), fg='#333', bg='#f0f0f0')
        self.video_label.image = None
    
    def show_status(self):
        """显示详细状态"""
        status_text = f"""
毛毛的状态：
🍖 饥饿度: {int(self.hunger)}%
😊 开心度: {int(self.happiness)}%
⚡ 精力值: {int(self.energy)}%
        """
        messagebox.showinfo("状态信息", status_text)
    
    def feed(self):
        """喂食"""
        if self.hunger < 15:
            self.show_emotion("🥰")
            self.root.after(2000, self.show_idle_state)
        else:
            self.show_emotion("😋")
            self.play_video('lick')
            self.hunger = max(0, self.hunger - 35)
            self.happiness = min(100, self.happiness + 12)
    
    def play(self):
        """玩耍"""
        if self.energy < 15:
            self.show_emotion("😫")
            self.play_video('tired')
            self.root.after(3000, self.show_idle_state)
        else:
            self.show_emotion("🏃")
            self.play_video('walk')
            self.hunger = min(100, self.hunger + 12)
            self.happiness = min(100, self.happiness + 20)
            self.energy = max(0, self.energy - 18)
    
    def tease(self):
        """逗它"""
        self.show_emotion("😸")
        self.play_video('stare')
        self.happiness = min(100, self.happiness + 15)
        self.energy = max(0, self.energy - 8)
    
    def sleep(self):
        """休息"""
        self.show_emotion("😴")
        self.play_video('tired')
        self.energy = min(100, self.energy + 45)
        self.hunger = min(100, self.hunger + 8)
        self.root.after(3500, self.show_idle_state)
    
    def pet(self):
        """爱抚/触摸"""
        self.show_emotion("😻")
        self.play_video('roll')
        self.happiness = min(100, self.happiness + 18)
        self.energy = max(0, self.energy - 5)

def main():
    root = tk.Tk()
    app = DesktopPet(root)
    app.show_idle_state()
    root.mainloop()

if __name__ == "__main__":
    main()
