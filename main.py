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
        self.root.geometry("600x700")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)
        
        # 设置视频路径 - 使用您的实际路径
        self.video_dir = r"C:\Users\联想\Desktop\bam"
        self.videos = {
            'lick': os.path.join(self.video_dir, '1.mp4'),      # 舔嘴唇
            'walk': os.path.join(self.video_dir, '2.mp4'),      # 来回走
            'stare': os.path.join(self.video_dir, '3.mp4'),     # 直视
            'roll': os.path.join(self.video_dir, '4.mp4'),      # 翻肚皮
            'tired': os.path.join(self.video_dir, '5.mp4'),     # 累了躺下
        }
        
        # 检查视频文件是否存在
        self.check_videos()
        
        # 宠物状态
        self.pet_name = "毛毛"
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.is_playing_video = False
        
        # 初始化UI
        self.setup_ui()
        self.update_status()
        
    def check_videos(self):
        """检查视频文件是否存在"""
        missing = []
        for action, path in self.videos.items():
            if not os.path.exists(path):
                missing.append(f"{action}: {path}")
        
        if missing:
            msg = "⚠️ 以下视频文件未找到：\n\n"
            msg += "\n".join(missing)
            msg += "\n\n请确保所有视频文件都在正确位置！"
            messagebox.showerror("视频文件错误", msg)
    
    def setup_ui(self):
        """设置用户界面"""
        # 标题
        title = tk.Label(
            self.root,
            text=f"🐱 欢迎来到 {self.pet_name} 的世界",
            font=("微软雅黑", 18, "bold"),
            bg='#f0f0f0',
            fg='#ff69b4'
        )
        title.pack(pady=15)
        
        # 视频显示区域
        self.video_label = tk.Label(
            self.root,
            bg='#e0e0e0',
            width=70,
            height=18,
            relief=tk.SUNKEN,
            borderwidth=3,
            text="点击下方按钮与毛毛互动 😊",
            font=("微软雅黑", 14),
            fg='#999'
        )
        self.video_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # 状态面板
        self.status_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.status_frame.pack(pady=10, fill=tk.X)
        
        # 饥饿度
        tk.Label(self.status_frame, text="🍖 饥饿度:", font=("微软雅黑", 11, "bold"), bg='#f0f0f0').pack(anchor=tk.W, padx=15)
        self.hunger_bar = tk.Canvas(self.status_frame, height=22, bg='white', highlightthickness=1, highlightbackground='#ccc')
        self.hunger_bar.pack(fill=tk.X, padx=15, pady=2)
        
        # 开心度
        tk.Label(self.status_frame, text="😊 开心度:", font=("微软雅黑", 11, "bold"), bg='#f0f0f0').pack(anchor=tk.W, padx=15)
        self.happiness_bar = tk.Canvas(self.status_frame, height=22, bg='white', highlightthickness=1, highlightbackground='#ccc')
        self.happiness_bar.pack(fill=tk.X, padx=15, pady=2)
        
        # 精力值
        tk.Label(self.status_frame, text="⚡ 精力值:", font=("微软雅黑", 11, "bold"), bg='#f0f0f0').pack(anchor=tk.W, padx=15)
        self.energy_bar = tk.Canvas(self.status_frame, height=22, bg='white', highlightthickness=1, highlightbackground='#ccc')
        self.energy_bar.pack(fill=tk.X, padx=15, pady=2)
        
        # 控制按钮区域
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=12, fill=tk.X)
        
        # 互动按钮
        btn_style = {"font": ("微软雅黑", 10, "bold"), "width": 11, "height": 2, "relief": tk.RAISED, "borderwidth": 2}
        
        tk.Button(
            button_frame,
            text="🍖 喂食",
            command=self.feed,
            bg='#ff9999',
            fg='white',
            activebackground='#ff6666',
            **btn_style
        ).pack(side=tk.LEFT, padx=4)
        
        tk.Button(
            button_frame,
            text="🎮 玩耍",
            command=self.play,
            bg='#99ccff',
            fg='white',
            activebackground='#66bbff',
            **btn_style
        ).pack(side=tk.LEFT, padx=4)
        
        tk.Button(
            button_frame,
            text="👀 逗它",
            command=self.tease,
            bg='#ffcc99',
            fg='white',
            activebackground='#ffbb66',
            **btn_style
        ).pack(side=tk.LEFT, padx=4)
        
        tk.Button(
            button_frame,
            text="😴 休息",
            command=self.sleep,
            bg='#ccccff',
            fg='white',
            activebackground='#aaaaff',
            **btn_style
        ).pack(side=tk.LEFT, padx=4)
        
        tk.Button(
            button_frame,
            text="❤️  爱抚",
            command=self.pet,
            bg='#ffcccc',
            fg='white',
            activebackground='#ffaaaa',
            **btn_style
        ).pack(side=tk.LEFT, padx=4)
    
    def update_status(self):
        """更新状态显示"""
        # 更新饥饿度条
        self.hunger_bar.delete("all")
        hunger_width = max(0, min(200, self.hunger * 2))
        self.hunger_bar.create_rectangle(0, 0, hunger_width, 22, fill='#ff6666', outline='')
        self.hunger_bar.create_text(205, 11, text=f"{int(self.hunger)}%", font=("微软雅黑", 10, "bold"), fill='#333')
        
        # 更新开心度条
        self.happiness_bar.delete("all")
        happiness_width = max(0, min(200, self.happiness * 2))
        self.happiness_bar.create_rectangle(0, 0, happiness_width, 22, fill='#66ff66', outline='')
        self.happiness_bar.create_text(205, 11, text=f"{int(self.happiness)}%", font=("微软雅黑", 10, "bold"), fill='#333')
        
        # 更新精力值条
        self.energy_bar.delete("all")
        energy_width = max(0, min(200, self.energy * 2))
        self.energy_bar.create_rectangle(0, 0, energy_width, 22, fill='#ffff66', outline='')
        self.energy_bar.create_text(205, 11, text=f"{int(self.energy)}%", font=("微软雅黑", 10, "bold"), fill='#333')
        
        # 每5秒自动衰减
        self.hunger = min(100, self.hunger + 0.8)
        self.happiness = max(0, self.happiness - 0.3)
        self.energy = max(0, self.energy - 0.2)
        
        self.root.after(5000, self.update_status)
    
    def play_video(self, video_name):
        """播放视频"""
        if self.is_playing_video:
            return
        
        if video_name not in self.videos:
            return
        
        video_path = self.videos[video_name]
        
        if not os.path.exists(video_path):
            self.show_emotion(f"❌ 找不到视频文件！\n{video_path}")
            return
        
        self.is_playing_video = True
        thread = threading.Thread(target=self._play_video_thread, args=(video_path,), daemon=True)
        thread.start()
    
    def _play_video_thread(self, video_path):
        """在单独线程中播放视频"""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                self.show_emotion("❌ 无法打开视频文件！")
                return
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_delay = max(10, int(1000 / fps)) if fps > 0 else 33
            
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # 调整帧大小以适应显示区域
                frame = cv2.resize(frame, (560, 320))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image)
                
                self.video_label.config(image=photo, text='')
                self.video_label.image = photo
                
                self.root.after(frame_delay)
            
            cap.release()
        except Exception as e:
            print(f"播放视频出错: {str(e)}")
            self.show_emotion(f"❌ 播放出错：{str(e)}")
        finally:
            self.is_playing_video = False
            self.root.after(500, self.show_idle_state)
    
    def show_idle_state(self):
        """显示待机状态"""
        self.video_label.config(bg='#e0e0e0', text="😊 毛毛在看着你呢～", font=("微软雅黑", 14), fg='#999')
        self.video_label.image = None
    
    def show_emotion(self, text):
        """显示情绪文本"""
        self.video_label.config(text=text, font=("微软雅黑", 13), fg='#333', bg='#e0e0e0')
        self.video_label.image = None
    
    def feed(self):
        """喂食"""
        if self.hunger < 15:
            self.show_emotion("🥰 我吃得很饱！\n现在不想吃了～")
            self.root.after(2000, self.show_idle_state)
        else:
            self.show_emotion("😋 呀！好好吃！")
            self.play_video('lick')
            self.hunger = max(0, self.hunger - 35)
            self.happiness = min(100, self.happiness + 12)
    
    def play(self):
        """玩耍"""
        if self.energy < 15:
            self.show_emotion("😫 我太累了...\n需要好好休息一下")
            self.play_video('tired')
            self.root.after(3000, self.show_idle_state)
        else:
            self.show_emotion("🏃 去玩耍咯！")
            self.play_video('walk')
            self.hunger = min(100, self.hunger + 12)
            self.happiness = min(100, self.happiness + 20)
            self.energy = max(0, self.energy - 18)
    
    def tease(self):
        """逗它"""
        if self.happiness > 70:
            self.show_emotion("😸 哈哈哈，你很有趣呢！")
            self.play_video('stare')
            self.happiness = min(100, self.happiness + 10)
            self.energy = max(0, self.energy - 8)
        else:
            self.show_emotion("👀 你想跟我玩吗？")
            self.play_video('stare')
            self.happiness = min(100, self.happiness + 15)
            self.energy = max(0, self.energy - 8)
    
    def sleep(self):
        """休息"""
        self.show_emotion("😴 困死我了...\nzzzzZZZZ...")
        self.play_video('tired')
        self.energy = min(100, self.energy + 45)
        self.hunger = min(100, self.hunger + 8)
        self.root.after(3500, self.show_idle_state)
    
    def pet(self):
        """爱抚/触摸"""
        self.show_emotion("😻 呼呼呼～好舒服啊！")
        self.play_video('roll')
        self.happiness = min(100, self.happiness + 18)
        self.energy = max(0, self.energy - 5)

def main():
    root = tk.Tk()
    app = DesktopPet(root)
    root.mainloop()

if __name__ == "__main__":
    main()
