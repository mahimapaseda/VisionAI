import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO
import threading
import time
from datetime import datetime

try:
    import mediapipe as mp
    import speech_recognition as sr
    import pyttsx3
    ADVANCED_FEATURES = True
except ImportError:
    ADVANCED_FEATURES = False

class VisionAIUnified:
    def __init__(self):
        # Core models
        self.yolo = YOLO('yolov8n.pt')
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Advanced features
        if ADVANCED_FEATURES:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(min_detection_confidence=0.7)
            self.mp_pose = mp.solutions.pose
            self.pose = self.mp_pose.Pose(min_detection_confidence=0.7)
            self.mp_draw = mp.solutions.drawing_utils
            self.recognizer = sr.Recognizer()
            self.tts = pyttsx3.init()
        
        # Camera state
        self.cap = None
        self.running = False
        self.recording = False
        self.out = None
        self.current_camera = 0
        
        # Mode selection
        self.current_mode = "optimized"  # "optimized" or "pro"
        
        # Performance
        self.frame_count = 0
        self.stats = {'objects': 0, 'faces': 0, 'gestures': 0, 'motion': 0}
        self.last_objects = []
        self.last_faces = []
        
        # Tracking
        self.tracked_objects = {}
        self.tracked_faces = {}
        self.object_id = 0
        self.face_id = 0
        
        # Motion detection
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2()
        
        # Data logging
        self.detection_log = []
        
        self.setup_gui()
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("🎯 VisionAI - Unified Smart Detection")
        self.root.geometry("1100x800")
        self.root.configure(bg='#1a252f')
        
        # Header with mode selector
        header_frame = tk.Frame(self.root, bg='#1a252f', height=80)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        header_frame.pack_propagate(False)
        
        # Title
        title = tk.Label(header_frame, text="🤖 VisionAI Unified", 
                        font=('Arial', 20, 'bold'), fg='#3498db', bg='#1a252f')
        title.pack(side=tk.LEFT, pady=20)
        
        # Mode selector
        mode_frame = tk.Frame(header_frame, bg='#1a252f')
        mode_frame.pack(side=tk.RIGHT, pady=20)
        
        tk.Label(mode_frame, text="Mode:", font=('Arial', 12, 'bold'), 
                fg='#ecf0f1', bg='#1a252f').pack(side=tk.LEFT, padx=(0, 10))
        
        self.mode_var = tk.StringVar(value="optimized")
        
        tk.Radiobutton(mode_frame, text="⚡ Optimized", variable=self.mode_var, value="optimized",
                      command=self.switch_mode, bg='#1a252f', fg='#27ae60', font=('Arial', 11, 'bold'),
                      selectcolor='#2c3e50', activebackground='#1a252f').pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(mode_frame, text="🚀 Pro", variable=self.mode_var, value="pro",
                      command=self.switch_mode, bg='#1a252f', fg='#e74c3c', font=('Arial', 11, 'bold'),
                      selectcolor='#2c3e50', activebackground='#1a252f').pack(side=tk.LEFT, padx=10)
        
        # Main container
        self.main_container = tk.Frame(self.root, bg='#1a252f')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Initialize detection variables
        self.detect_objects = tk.BooleanVar(value=True)
        self.detect_faces = tk.BooleanVar(value=True)
        self.detect_motion = tk.BooleanVar()
        self.privacy_mode = tk.BooleanVar()
        self.gesture_var = tk.BooleanVar()
        self.pose_var = tk.BooleanVar()
        self.voice_var = tk.BooleanVar()
        
        self.setup_optimized_mode()
    
    def switch_mode(self):
        # Clear current interface
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        self.current_mode = self.mode_var.get()
        
        if self.current_mode == "optimized":
            self.setup_optimized_mode()
        else:
            self.setup_pro_mode()
    
    def setup_optimized_mode(self):
        # Controls
        ctrl_frame = tk.LabelFrame(self.main_container, text="🎮 Quick Controls", 
                                  font=('Arial', 11, 'bold'), fg='#3498db', bg='#34495e')
        ctrl_frame.pack(fill=tk.X, pady=(0, 10))
        
        btn_frame = tk.Frame(ctrl_frame, bg='#34495e')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="▶ Start", command=self.start,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5, relief='flat').pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="⏹ Stop", command=self.stop,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5, relief='flat').pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="⏺ Record", command=self.toggle_record,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5, relief='flat').pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="📸 Shot", command=self.screenshot,
                 bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5, relief='flat').pack(side=tk.LEFT, padx=5)
        
        # Detection options
        det_frame = tk.LabelFrame(self.main_container, text="🔍 Detection Options",
                                 font=('Arial', 10, 'bold'), fg='#3498db', bg='#34495e')
        det_frame.pack(fill=tk.X, pady=(0, 10))
        
        opt_frame = tk.Frame(det_frame, bg='#34495e')
        opt_frame.pack(pady=10)
        
        tk.Checkbutton(opt_frame, text="🎯 Objects", variable=self.detect_objects,
                      bg='#34495e', fg='#ecf0f1', font=('Arial', 9),
                      selectcolor='#2c3e50').pack(side=tk.LEFT, padx=15)
        tk.Checkbutton(opt_frame, text="👤 Faces", variable=self.detect_faces,
                      bg='#34495e', fg='#ecf0f1', font=('Arial', 9),
                      selectcolor='#2c3e50').pack(side=tk.LEFT, padx=15)
        tk.Checkbutton(opt_frame, text="🏃 Motion", variable=self.detect_motion,
                      bg='#34495e', fg='#ecf0f1', font=('Arial', 9),
                      selectcolor='#2c3e50').pack(side=tk.LEFT, padx=15)
        tk.Checkbutton(opt_frame, text="🔒 Privacy", variable=self.privacy_mode,
                      bg='#34495e', fg='#ecf0f1', font=('Arial', 9),
                      selectcolor='#2c3e50').pack(side=tk.LEFT, padx=15)
        
        # Video display
        video_frame = tk.LabelFrame(self.main_container, text="📹 Live Feed",
                                   font=('Arial', 10, 'bold'), fg='#3498db', bg='#34495e')
        video_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.video_label = tk.Label(video_frame, bg='#2c3e50', text="Camera Feed Will Appear Here",
                                   fg='#7f8c8d', font=('Arial', 12))
        self.video_label.pack(pady=20)
        
        # Status and stats
        bottom_frame = tk.Frame(self.main_container, bg='#1a252f')
        bottom_frame.pack(fill=tk.X)
        
        # Status
        status_frame = tk.LabelFrame(bottom_frame, text="📊 Status",
                                    font=('Arial', 9, 'bold'), fg='#3498db', bg='#34495e')
        status_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        status_inner = tk.Frame(status_frame, bg='#34495e')
        status_inner.pack(pady=5)
        
        self.status = tk.Label(status_inner, text="🟢 Ready", bg='#34495e', fg='#ecf0f1', font=('Arial', 9))
        self.status.pack(side=tk.LEFT)
        
        self.fps_label = tk.Label(status_inner, text="⚡ FPS: 0", bg='#34495e', fg='#ecf0f1', font=('Arial', 9))
        self.fps_label.pack(side=tk.RIGHT)
        
        # Stats
        stats_frame = tk.LabelFrame(bottom_frame, text="📈 Stats",
                                   font=('Arial', 9, 'bold'), fg='#3498db', bg='#34495e')
        stats_frame.pack(side=tk.RIGHT, padx=(5, 0))
        
        stats_inner = tk.Frame(stats_frame, bg='#34495e')
        stats_inner.pack(pady=5)
        
        self.obj_label = tk.Label(stats_inner, text="🎯 Objects: 0", bg='#34495e', fg='#ecf0f1', font=('Arial', 9))
        self.obj_label.pack(side=tk.LEFT, padx=10)
        
        self.face_label = tk.Label(stats_inner, text="👤 Faces: 0", bg='#34495e', fg='#ecf0f1', font=('Arial', 9))
        self.face_label.pack(side=tk.LEFT, padx=10)
        
        self.motion_label = tk.Label(stats_inner, text="🏃 Motion: 0", bg='#34495e', fg='#ecf0f1', font=('Arial', 9))
        self.motion_label.pack(side=tk.LEFT, padx=10)
    
    def setup_pro_mode(self):
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Pro.TNotebook', background='#1a252f')
        style.configure('Pro.TNotebook.Tab', background='#34495e', foreground='#ecf0f1', padding=[15, 8])
        style.map('Pro.TNotebook.Tab', background=[('selected', '#3498db')])
        
        # Notebook
        notebook = ttk.Notebook(self.main_container, style='Pro.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Camera tab
        camera_tab = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(camera_tab, text="📹 Camera")
        
        # Settings tab
        settings_tab = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(settings_tab, text="⚙️ Settings")
        
        # Analytics tab
        analytics_tab = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(analytics_tab, text="📊 Analytics")
        
        self.setup_camera_tab(camera_tab)
        self.setup_settings_tab(settings_tab)
        self.setup_analytics_tab(analytics_tab)
    
    def setup_camera_tab(self, parent):
        # Controls
        control_frame = tk.LabelFrame(parent, text="🎮 Advanced Controls", 
                                     font=('Arial', 11, 'bold'), fg='#3498db', bg='#34495e')
        control_frame.pack(fill=tk.X, padx=15, pady=15)
        
        btn_container = tk.Frame(control_frame, bg='#34495e')
        btn_container.pack(pady=15)
        
        tk.Button(btn_container, text="▶ Start Camera", command=self.start,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=8, relief='flat').pack(side=tk.LEFT, padx=8)
        
        tk.Button(btn_container, text="⏹ Stop Camera", command=self.stop,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=8, relief='flat').pack(side=tk.LEFT, padx=8)
        
        tk.Button(btn_container, text="⏺ Record Video", command=self.toggle_record,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=8, relief='flat').pack(side=tk.LEFT, padx=8)
        
        tk.Button(btn_container, text="📸 Screenshot", command=self.screenshot,
                 bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=8, relief='flat').pack(side=tk.LEFT, padx=8)
        
        tk.Button(btn_container, text="🔄 Switch Cam", command=self.switch_camera,
                 bg='#34495e', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=8, relief='flat').pack(side=tk.LEFT, padx=8)
        
        # Video display
        video_frame = tk.LabelFrame(parent, text="📹 Professional Camera Feed",
                                   font=('Arial', 11, 'bold'), fg='#3498db', bg='#34495e')
        video_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.video_label = tk.Label(video_frame, bg='#2c3e50', 
                                   text="Professional camera feed will appear here",
                                   fg='#7f8c8d', font=('Arial', 14))
        self.video_label.pack(pady=30)
        
        # Status
        status_frame = tk.Frame(parent, bg='#2c3e50')
        status_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        status_left = tk.LabelFrame(status_frame, text="📊 System Status",
                                   font=('Arial', 9, 'bold'), fg='#3498db', bg='#34495e')
        status_left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.status = tk.Label(status_left, text="🟢 Professional Mode Ready", 
                              bg='#34495e', fg='#ecf0f1', font=('Arial', 10))
        self.status.pack(pady=8)
        
        status_right = tk.LabelFrame(status_frame, text="⚡ Performance",
                                    font=('Arial', 9, 'bold'), fg='#3498db', bg='#34495e')
        status_right.pack(side=tk.RIGHT)
        
        self.fps_label = tk.Label(status_right, text="FPS: 0", 
                                 bg='#34495e', fg='#ecf0f1', font=('Arial', 10))
        self.fps_label.pack(pady=8, padx=15)
    
    def setup_settings_tab(self, parent):
        # Detection settings
        detection_frame = tk.LabelFrame(parent, text="🔍 AI Detection Settings",
                                       font=('Arial', 12, 'bold'), fg='#3498db', bg='#34495e')
        detection_frame.pack(fill=tk.X, padx=15, pady=15)
        
        settings_grid = tk.Frame(detection_frame, bg='#34495e')
        settings_grid.pack(pady=20, padx=20)
        
        # Core detection
        tk.Label(settings_grid, text="Core Detection:", font=('Arial', 11, 'bold'),
                fg='#ecf0f1', bg='#34495e').grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        tk.Checkbutton(settings_grid, text="🎯 Object Detection", variable=self.detect_objects,
                      bg='#34495e', fg='#ecf0f1', font=('Arial', 10), selectcolor='#2c3e50').grid(row=1, column=0, sticky=tk.W, padx=(20, 40), pady=5)
        tk.Checkbutton(settings_grid, text="👤 Face Detection", variable=self.detect_faces,
                      bg='#34495e', fg='#ecf0f1', font=('Arial', 10), selectcolor='#2c3e50').grid(row=1, column=1, sticky=tk.W, pady=5)
        tk.Checkbutton(settings_grid, text="🏃 Motion Detection", variable=self.detect_motion,
                      bg='#34495e', fg='#ecf0f1', font=('Arial', 10), selectcolor='#2c3e50').grid(row=2, column=0, sticky=tk.W, padx=(20, 40), pady=5)
        tk.Checkbutton(settings_grid, text="🔒 Privacy Mode", variable=self.privacy_mode,
                      bg='#34495e', fg='#ecf0f1', font=('Arial', 10), selectcolor='#2c3e50').grid(row=2, column=1, sticky=tk.W, pady=5)
        
        if ADVANCED_FEATURES:
            tk.Label(settings_grid, text="Advanced Features:", font=('Arial', 11, 'bold'),
                    fg='#ecf0f1', bg='#34495e').grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
            
            tk.Checkbutton(settings_grid, text="👋 Gesture Recognition", variable=self.gesture_var,
                          bg='#34495e', fg='#ecf0f1', font=('Arial', 10), selectcolor='#2c3e50').grid(row=4, column=0, sticky=tk.W, padx=(20, 40), pady=5)
            tk.Checkbutton(settings_grid, text="🧘 Pose Estimation", variable=self.pose_var,
                          bg='#34495e', fg='#ecf0f1', font=('Arial', 10), selectcolor='#2c3e50').grid(row=4, column=1, sticky=tk.W, pady=5)
            tk.Checkbutton(settings_grid, text="🎤 Voice Control", variable=self.voice_var,
                          bg='#34495e', fg='#ecf0f1', font=('Arial', 10), selectcolor='#2c3e50').grid(row=5, column=0, sticky=tk.W, padx=(20, 40), pady=5)
        
        # Data management
        export_frame = tk.LabelFrame(parent, text="📁 Data Management",
                                    font=('Arial', 12, 'bold'), fg='#3498db', bg='#34495e')
        export_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        export_buttons = tk.Frame(export_frame, bg='#34495e')
        export_buttons.pack(pady=15)
        
        tk.Button(export_buttons, text="📤 Export Log", command=self.export_log,
                 bg='#16a085', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=8, relief='flat').pack(side=tk.LEFT, padx=10)
        
        tk.Button(export_buttons, text="🗑️ Clear Data", command=self.clear_log,
                 bg='#e67e22', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=8, relief='flat').pack(side=tk.LEFT, padx=10)
    
    def setup_analytics_tab(self, parent):
        # Stats cards
        counter_frame = tk.LabelFrame(parent, text="📈 Detection Statistics",
                                     font=('Arial', 12, 'bold'), fg='#3498db', bg='#34495e')
        counter_frame.pack(fill=tk.X, padx=15, pady=15)
        
        stats_container = tk.Frame(counter_frame, bg='#34495e')
        stats_container.pack(pady=20)
        
        # Cards
        obj_card = tk.Frame(stats_container, bg='#27ae60', relief='flat', bd=2)
        obj_card.pack(side=tk.LEFT, padx=15, pady=10)
        
        tk.Label(obj_card, text="🎯", font=('Arial', 20), bg='#27ae60', fg='white').pack(pady=(10, 5))
        self.obj_label = tk.Label(obj_card, text="Objects: 0", font=('Arial', 12, 'bold'),
                                 bg='#27ae60', fg='white')
        self.obj_label.pack(pady=(0, 10), padx=20)
        
        face_card = tk.Frame(stats_container, bg='#3498db', relief='flat', bd=2)
        face_card.pack(side=tk.LEFT, padx=15, pady=10)
        
        tk.Label(face_card, text="👤", font=('Arial', 20), bg='#3498db', fg='white').pack(pady=(10, 5))
        self.face_label = tk.Label(face_card, text="Faces: 0", font=('Arial', 12, 'bold'),
                                  bg='#3498db', fg='white')
        self.face_label.pack(pady=(0, 10), padx=20)
        
        motion_card = tk.Frame(stats_container, bg='#f39c12', relief='flat', bd=2)
        motion_card.pack(side=tk.LEFT, padx=15, pady=10)
        
        tk.Label(motion_card, text="🏃", font=('Arial', 20), bg='#f39c12', fg='white').pack(pady=(10, 5))
        self.motion_label = tk.Label(motion_card, text="Motion: 0", font=('Arial', 12, 'bold'),
                                    bg='#f39c12', fg='white')
        self.motion_label.pack(pady=(0, 10), padx=20)
        
        # Detection log
        recent_frame = tk.LabelFrame(parent, text="🕰️ Detection Log",
                                    font=('Arial', 12, 'bold'), fg='#3498db', bg='#34495e')
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        tree_frame = tk.Frame(recent_frame, bg='#34495e')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.detection_tree = ttk.Treeview(tree_frame, columns=('Time', 'Type', 'Details'), show='headings', height=10)
        self.detection_tree.heading('Time', text='🕰️ Time')
        self.detection_tree.heading('Type', text='🏷️ Type')
        self.detection_tree.heading('Details', text='📝 Details')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.detection_tree.yview)
        self.detection_tree.configure(yscrollcommand=scrollbar.set)
        
        self.detection_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def detect_objects_in_frame(self, frame):
        if not self.detect_objects.get():
            return frame
        
        if self.frame_count % 2 == 0:
            # Use higher resolution for better accuracy
            small = cv2.resize(frame, (640, 640))
            
            # Enhanced YOLO parameters for accuracy
            results = self.yolo(small, 
                              conf=0.4,        # Lower confidence for more detections
                              iou=0.5,         # Higher IoU for better filtering
                              max_det=50,      # Limit detections
                              verbose=False,
                              agnostic_nms=True)  # Better NMS
            
            h, w = frame.shape[:2]
            scale_x, scale_y = w / 640, h / 640
            
            current_objects = []
            
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1*scale_x), int(y1*scale_y), int(x2*scale_x), int(y2*scale_y)
                        conf = float(box.conf[0])
                        cls = int(box.cls[0])
                        
                        # Skip person class and low confidence
                        if cls == 0 or conf < 0.5:
                            continue
                        
                        # Filter by box size (remove tiny detections)
                        box_area = (x2 - x1) * (y2 - y1)
                        if box_area < 400:  # Minimum 20x20 pixels
                            continue
                        
                        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
                        obj_class = self.yolo.names[cls]
                        obj_id = self.get_object_id(center_x, center_y, obj_class, conf)
                        
                        if obj_id is not None:
                            label = f"{obj_class}_{obj_id}: {conf:.2f}"
                            current_objects.append((x1, y1, x2, y2, label, conf))
                            
                            # Log new detections
                            if obj_id not in [item[4] for item in self.last_objects if len(item) > 4]:
                                self.log_detection('Object', f"{obj_class}_{obj_id} (conf: {conf:.2f})")
            
            self.last_objects = current_objects
            self.cleanup_old_objects()
        
        # Draw with confidence-based styling
        for x1, y1, x2, y2, label, conf in self.last_objects:
            # Color intensity based on confidence
            intensity = int(conf * 255)
            color = (0, intensity, 0)
            thickness = 2 if conf > 0.7 else 1
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
            
            # Background for text
            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            cv2.rectangle(frame, (x1, y1-text_size[1]-8), (x1+text_size[0]+4, y1), color, -1)
            cv2.putText(frame, label, (x1+2, y1-4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def detect_faces_in_frame(self, frame):
        if not self.detect_faces.get():
            return frame
        
        if self.frame_count % 2 == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(40, 40))
            
            current_faces = []
            
            for (x, y, w, h) in faces:
                center_x, center_y = x + w//2, y + h//2
                face_id = self.get_face_id(center_x, center_y)
                
                current_faces.append((x, y, w, h, face_id))
                
                # Log new face detections
                if face_id not in [item[4] for item in self.last_faces if len(item) > 4]:
                    self.log_detection('Face', f"Face_{face_id} detected")
            
            self.last_faces = current_faces
            self.cleanup_old_faces()
        
        for (x, y, w, h, face_id) in self.last_faces:
            if self.privacy_mode.get():
                face_region = frame[y:y+h, x:x+w]
                face_region = cv2.GaussianBlur(face_region, (51, 51), 30)
                frame[y:y+h, x:x+w] = face_region
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, "PRIVATE", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, f"Face_{face_id}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
        
        return frame
    
    def detect_motion_in_frame(self, frame):
        if not self.detect_motion.get():
            return frame
        
        fg_mask = self.bg_subtractor.apply(frame)
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                cv2.putText(frame, "MOTION", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                self.stats['motion'] += 1
                self.log_detection('Motion', f"Area: {cv2.contourArea(contour):.0f} pixels")
        
        return frame
    
    def get_object_id(self, x, y, obj_class, confidence):
        min_dist = float('inf')
        closest_id = None
        
        # Dynamic tracking distance based on object class
        tracking_distances = {
            'car': 150, 'truck': 150, 'bus': 150, 'motorcycle': 100,
            'bottle': 50, 'cup': 50, 'bowl': 50, 'wine glass': 50,
            'laptop': 80, 'mouse': 40, 'keyboard': 80, 'cell phone': 60,
            'book': 60, 'clock': 60, 'vase': 60
        }
        max_distance = tracking_distances.get(obj_class, 80)
        
        for obj_id, (ox, oy, oclass, frame_seen, conf_history) in self.tracked_objects.items():
            if oclass == obj_class:
                dist = ((x - ox) ** 2 + (y - oy) ** 2) ** 0.5
                if dist < max_distance and dist < min_dist:
                    min_dist = dist
                    closest_id = obj_id
        
        if closest_id is not None:
            # Update existing object with confidence tracking
            _, _, oclass, _, conf_history = self.tracked_objects[closest_id]
            conf_history.append(confidence)
            if len(conf_history) > 5:  # Keep last 5 confidence scores
                conf_history.pop(0)
            
            self.tracked_objects[closest_id] = (x, y, obj_class, self.frame_count, conf_history)
            return closest_id
        else:
            # Only create new object if confidence is high enough
            if confidence > 0.6:
                self.object_id += 1
                self.tracked_objects[self.object_id] = (x, y, obj_class, self.frame_count, [confidence])
                self.stats['objects'] += 1
                return self.object_id
            return None
    
    def get_face_id(self, x, y):
        min_dist = float('inf')
        closest_id = None
        
        for face_id, (fx, fy, frame_seen) in self.tracked_faces.items():
            dist = ((x - fx) ** 2 + (y - fy) ** 2) ** 0.5
            if dist < 80 and dist < min_dist:
                min_dist = dist
                closest_id = face_id
        
        if closest_id is not None:
            self.tracked_faces[closest_id] = (x, y, self.frame_count)
            return closest_id
        else:
            self.face_id += 1
            self.tracked_faces[self.face_id] = (x, y, self.frame_count)
            self.stats['faces'] += 1
            return self.face_id
    
    def cleanup_old_objects(self):
        to_remove = []
        for obj_id, (x, y, obj_class, frame_seen, conf_history) in self.tracked_objects.items():
            age = self.frame_count - frame_seen
            avg_confidence = sum(conf_history) / len(conf_history) if conf_history else 0
            
            # Remove objects based on age and confidence
            if age > 20 or avg_confidence < 0.4:
                to_remove.append(obj_id)
        
        for obj_id in to_remove:
            del self.tracked_objects[obj_id]
        
        # Limit total objects to prevent memory issues
        if len(self.tracked_objects) > 30:
            # Remove lowest confidence objects
            sorted_objects = sorted(self.tracked_objects.items(), 
                                  key=lambda x: sum(x[1][4])/len(x[1][4]))
            for obj_id, _ in sorted_objects[:5]:
                if obj_id in self.tracked_objects:
                    del self.tracked_objects[obj_id]
    
    def cleanup_old_faces(self):
        to_remove = []
        for face_id, (x, y, frame_seen) in self.tracked_faces.items():
            if self.frame_count - frame_seen > 30:
                to_remove.append(face_id)
        
        for face_id in to_remove:
            del self.tracked_faces[face_id]
    
    def start(self):
        if not self.running:
            self.cap = cv2.VideoCapture(self.current_camera)
            if self.cap.isOpened():
                self.running = True
                mode_text = "Optimized" if self.current_mode == "optimized" else "Professional"
                self.status.config(text=f"🔴 {mode_text} Mode Active")
                self.process_frame()
            else:
                messagebox.showerror("Error", "Cannot open camera")
    
    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
        if self.out:
            self.out.release()
        self.status.config(text="🟡 Stopped - Ready to Start")
    
    def switch_camera(self):
        self.current_camera = (self.current_camera + 1) % 3
        if self.running:
            self.stop()
            time.sleep(0.5)
            self.start()
    
    def toggle_record(self):
        if not self.recording and self.running:
            os.makedirs("recordings", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recordings/video_{timestamp}.avi"
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
            self.recording = True
            self.status.config(text=f"🔴 Recording: {filename}")
        else:
            self.recording = False
            if self.out:
                self.out.release()
            mode_text = "Optimized" if self.current_mode == "optimized" else "Professional"
            self.status.config(text=f"🟡 {mode_text} Mode Active")
    
    def screenshot(self):
        if self.running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                os.makedirs("screenshots", exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshots/shot_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                messagebox.showinfo("Screenshot", f"Saved: {filename}")
    
    def process_frame(self):
        if self.running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.frame_count += 1
                start_time = time.time()
                
                frame = self.detect_motion_in_frame(frame)
                frame = self.detect_objects_in_frame(frame)
                frame = self.detect_faces_in_frame(frame)
                
                if self.recording and self.out:
                    self.out.write(frame)
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_rgb = cv2.resize(frame_rgb, (640, 480))
                
                img = Image.fromarray(frame_rgb)
                photo = ImageTk.PhotoImage(img)
                
                self.video_label.config(image=photo)
                self.video_label.image = photo
                
                fps = 1.0 / (time.time() - start_time) if time.time() - start_time > 0 else 0
                fps_text = f"⚡ FPS: {fps:.1f}" if self.current_mode == "optimized" else f"FPS: {fps:.1f}"
                self.fps_label.config(text=fps_text)
                
                # Update stats
                if self.current_mode == "optimized":
                    self.obj_label.config(text=f"🎯 Objects: {self.stats['objects']}")
                    self.face_label.config(text=f"👤 Faces: {self.stats['faces']}")
                    self.motion_label.config(text=f"🏃 Motion: {self.stats['motion']}")
                else:
                    self.obj_label.config(text=f"Objects: {self.stats['objects']}")
                    self.face_label.config(text=f"Faces: {self.stats['faces']}")
                    self.motion_label.config(text=f"Motion: {self.stats['motion']}")
                
            self.root.after(30, self.process_frame)
    
    def log_detection(self, detection_type, details):
        """Log detection events"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.detection_log.append({
            'timestamp': timestamp,
            'type': detection_type,
            'details': details
        })
        
        # Update tree view if in Pro mode
        if self.current_mode == "pro" and hasattr(self, 'detection_tree'):
            try:
                self.detection_tree.insert('', 0, values=(timestamp, detection_type, details))
                
                # Keep only last 50 entries in tree
                items = self.detection_tree.get_children()
                if len(items) > 50:
                    self.detection_tree.delete(items[-1])
            except:
                pass
        
        # Keep only last 100 entries in log
        if len(self.detection_log) > 100:
            self.detection_log.pop(0)
    
    def export_log(self):
        """Export detection log to CSV"""
        if not self.detection_log:
            messagebox.showwarning("Export", "No detection data to export")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Detection Log"
        )
        
        if filename:
            try:
                import csv
                with open(filename, 'w', newline='') as csvfile:
                    fieldnames = ['timestamp', 'type', 'details']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.detection_log)
                messagebox.showinfo("Export", f"Detection log exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export log:\n{str(e)}")
    
    def clear_log(self):
        """Clear detection log and statistics"""
        self.detection_log.clear()
        self.stats = {'objects': 0, 'faces': 0, 'gestures': 0, 'motion': 0}
        
        # Clear tree view if in Pro mode
        if self.current_mode == "pro" and hasattr(self, 'detection_tree'):
            try:
                for item in self.detection_tree.get_children():
                    self.detection_tree.delete(item)
            except:
                pass
        
        messagebox.showinfo("Clear", "Detection log and statistics cleared")
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    
    def on_close(self):
        self.stop()
        self.root.destroy()

if __name__ == "__main__":
    app = VisionAIUnified()
    app.run()