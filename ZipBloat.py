import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import zipfile
import os
import threading
import configparser
import shutil
import stat
import logging
from logging.handlers import RotatingFileHandler
import time
import datetime
import sys


class ZipBloatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ZipBloat - ZIP文件体积放大工具 | Geekline")
        self.root.geometry("750x450")
        self.root.resizable(False, False)

        self.language = tk.StringVar(value="zh")
        self.lang_texts = {
            "zh": {
                "title": "ZipBloat - ZIP文件体积放大工具 | Geekline",
                "original_file": "原ZIP文件:",
                "output_file": "输出ZIP文件:",
                "browse": "浏览",
                "target_size": "目标放大体积 (GB):",
                "size_tip": "(建议1-20GB，过大会耗时较长)",
                "zoom_method": "放大方式:",
                "empty_block": "添加空块",
                "nest_zip": "嵌套ZIP",
                "append_junk": "尾部追加垃圾数据",
                "zip_bomb": "ZIP炸弹模式",
                "start": "开始生成",
                "cancel": "取消",
                "status_ready": "状态: 就绪",
                "status_running": "状态: 正在生成...",
                "status_canceled": "状态: 已取消",
                "status_completed": "状态: 生成完成！",
                "status_failed": "状态: 生成失败",
                "warn_running": "提示",
                "warn_running_msg": "任务正在运行中，请等待！",
                "err_num": "错误",
                "err_num_msg": "目标体积必须是数字！",
                "err_file_not_exist": "文件不存在！请选择有效的原ZIP文件。",
                "err_file_format": "格式错误！所选文件不是ZIP格式。",
                "err_output_path": "请选择输出文件路径！",
                "err_param": "参数错误！目标体积请设置为0-100GB之间。",
                "err_permission": "权限拒绝！输出路径无写入权限，请更换路径。",
                "warn_disk_space": "警告",
                "warn_disk_space_msg": "磁盘空间不足！可能导致生成失败，是否继续？",
                "success_title": "成功",
                "success_msg": "ZIP文件已生成：\n",
                "fail_title": "错误",
                "fail_msg": "生成失败：\n",
                "err_perm_detail": "权限错误：无法写入文件，请检查路径权限。",
                "err_zip_format": "格式错误：原文件不是有效的ZIP文件。",
                "err_disk_full": "磁盘错误：目标磁盘空间不足。",
                "err_system": "系统错误：",
                "err_unknown": "未知错误：",
                "lang_zh": "中文",
                "lang_en": "English",
                "console_title": "ZipBloat - ZIP文件体积放大工具",
                "console_author": "编写: Geekline",
                "console_website": " geekline.pages.dev",
                "help_title": "使用说明",
                "help_content": "ZipBloat 使用说明\n\n1. 选择原ZIP文件：点击浏览按钮选择需要放大的ZIP文件\n2. 设置输出路径：系统会自动生成输出路径，也可以手动修改\n3. 设置目标体积：输入需要放大到的目标体积（GB）\n4. 选择放大方式：\n   - 添加空块：在ZIP中添加大量空文件\n   - 嵌套ZIP：创建多层嵌套的ZIP结构\n   - 尾部追加垃圾数据：在ZIP文件尾部追加垃圾数据\n   - ZIP炸弹模式：生成体积很小但解压后会爆炸的ZIP\n5. 点击开始生成：等待生成完成\n\n注意事项：\n- 目标体积建议设置在1-20GB之间\n- 生成过程中可以取消操作\n- 确保输出路径有写入权限\n- ZIP炸弹模式请谨慎使用，仅用于测试目的",
                "help_btn": "帮助"
            },
            "en": {
                "title": "ZipBloat - ZIP File Size Enlarger | Geekline",
                "original_file": "Original ZIP File:",
                "output_file": "Output ZIP File:",
                "browse": "Browse",
                "target_size": "Target Size (GB):",
                "size_tip": "(Recommended 1-20GB, larger sizes take longer)",
                "zoom_method": "Enlarge Method:",
                "empty_block": "Add Empty Blocks",
                "nest_zip": "Nested ZIP",
                "append_junk": "Append Junk Data",
                "zip_bomb": "ZIP Bomb Mode",
                "start": "Start Generating",
                "cancel": "Cancel",
                "status_ready": "Status: Ready",
                "status_running": "Status: Generating...",
                "status_canceled": "Status: Canceled",
                "status_completed": "Status: Generated!",
                "status_failed": "Status: Failed",
                "warn_running": "Warning",
                "warn_running_msg": "Task is running, please wait!",
                "err_num": "Error",
                "err_num_msg": "Target size must be a number!",
                "err_file_not_exist": "File not found! Please select a valid ZIP file.",
                "err_file_format": "Format error! Selected file is not a ZIP file.",
                "err_output_path": "Please select output file path!",
                "err_param": "Parameter error! Target size must be between 0-100GB.",
                "err_permission": "Permission denied! No write permission for output path, please change path.",
                "warn_disk_space": "Warning",
                "warn_disk_space_msg": "Insufficient disk space! May cause generation failure, continue?",
                "success_title": "Success",
                "success_msg": "ZIP file generated:\n",
                "fail_title": "Error",
                "fail_msg": "Generation failed:\n",
                "err_perm_detail": "Permission error: Cannot write file, check path permission.",
                "err_zip_format": "Format error: Original file is not a valid ZIP file.",
                "err_disk_full": "Disk error: Insufficient disk space on target drive.",
                "err_system": "System error:",
                "err_unknown": "Unknown error:",
                "lang_zh": "中文",
                "lang_en": "English",
                "console_title": "ZipBloat - ZIP File Size Enlarger",
                "console_author": "Author: Geekline",
                "console_website": "geekline.pages.dev",
                "help_title": "Usage Instructions",
                "help_content": "ZipBloat Usage Instructions\n\n1. Select Original ZIP File: Click browse button to select the ZIP file to enlarge\n2. Set Output Path: System will automatically generate output path, or you can modify it manually\n3. Set Target Size: Enter the target size (GB) to enlarge to\n4. Select Enlarge Method:\n   - Add Empty Blocks: Add many empty files to ZIP\n   - Nested ZIP: Create multi-layer nested ZIP structure\n   - Append Junk Data: Append junk data to the end of ZIP file\n   - ZIP Bomb Mode: Generate a small ZIP that explodes when extracted\n5. Click Start Generating: Wait for completion\n\nNotes:\n- Recommended target size: 1-20GB\n- You can cancel operation during generation\n- Ensure write permission for output path\n- Use ZIP Bomb Mode with caution, only for testing purposes",
                "help_btn": "Help"
            }
        }

        self.original_zip_path = tk.StringVar()
        self.output_zip_path = tk.StringVar()
        self.target_size_gb = tk.DoubleVar(value=1.0)
        self.zoom_method = tk.StringVar(value="append_junk")
        self.is_running = False
        self.last_click_time = 0
        self.click_debounce_delay = 500

        self.config_path = os.path.join(os.path.expanduser("~"), "ZipBloat_config.ini")
        self._init_log()
        self._load_config()
        self._create_widgets()
        self._update_lang()
        
        lang = self.language.get()
        texts = self.lang_texts[lang]
        self.method_combobox['values'] = [texts["empty_block"], texts["nest_zip"], texts["append_junk"], texts["zip_bomb"]]
        current_method = self.zoom_method.get()
        if current_method == "empty_block":
            self.method_combobox.set(texts["empty_block"])
        elif current_method == "nest_zip":
            self.method_combobox.set(texts["nest_zip"])
        elif current_method == "append_junk":
            self.method_combobox.set(texts["append_junk"])
        else:
            self.method_combobox.set(texts["zip_bomb"])

    def _init_log(self):
        log_dir = os.path.join(os.path.expanduser("~"), "ZipBloat", "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"zipbloat_{datetime.datetime.now().strftime('%Y%m%d')}.log")

        self.logger = logging.getLogger("ZipBloat")
        self.logger.setLevel(logging.INFO)
    
        handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(handler)

        self.logger.info("=" * 50)
        self.logger.info("ZipBloat started")
        self.logger.info("=" * 50)

    def _create_widgets(self):
        style = ttk.Style(self.root)
        style.configure("TButton", font=("Microsoft YaHei", 9), padding=5)
        style.configure("TLabel", font=("Microsoft YaHei", 9))
        style.configure("TEntry", font=("Microsoft YaHei", 9))
        style.configure("TRadiobutton", font=("Microsoft YaHei", 9))
        style.configure("TProgressbar", height=10)
        style.configure("TCombobox", font=("Microsoft YaHei", 9))

        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)

        lang_frame = ttk.Frame(control_frame)
        lang_frame.pack(side=tk.RIGHT, padx=10)
        self.btn_help = ttk.Button(lang_frame, text="", command=self._show_help, width=6)
        self.btn_help.pack(side=tk.LEFT, padx=5)
        self.lang_combobox = ttk.Combobox(
            lang_frame,
            textvariable=self.language,
            values=["中文", "English"],
            state="readonly",
            width=8
        )
        self.lang_combobox.pack(side=tk.LEFT, padx=5)
        self.lang_combobox.bind("<<ComboboxSelected>>", self._update_lang)
        if self.language.get() == "zh":
            self.lang_combobox.set("中文")
        else:
            self.lang_combobox.set("English")

        frame1 = ttk.Frame(self.root, padding="10")
        frame1.pack(fill=tk.X)
        self.label_original = ttk.Label(frame1, text="")
        self.label_original.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_original = ttk.Entry(frame1, textvariable=self.original_zip_path, width=50)
        self.entry_original.grid(row=0, column=1, padx=5, pady=5)
        self._add_context_menu(self.entry_original)
        self.btn_browse_original = ttk.Button(frame1, text="", command=self._select_original_zip, width=8)
        self.btn_browse_original.grid(row=0, column=2, padx=5, pady=5)

        frame2 = ttk.Frame(self.root, padding="10")
        frame2.pack(fill=tk.X)
        self.label_output = ttk.Label(frame2, text="")
        self.label_output.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_output = ttk.Entry(frame2, textvariable=self.output_zip_path, width=50)
        self.entry_output.grid(row=0, column=1, padx=5, pady=5)
        self._add_context_menu(self.entry_output)
        self.btn_browse_output = ttk.Button(frame2, text="", command=self._select_output_zip, width=8)
        self.btn_browse_output.grid(row=0, column=2, padx=5, pady=5)

        frame3 = ttk.Frame(self.root, padding="10")
        frame3.pack(fill=tk.X)
        self.label_size = ttk.Label(frame3, text="")
        self.label_size.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_size = ttk.Entry(frame3, textvariable=self.target_size_gb, width=10)
        self.entry_size.grid(row=0, column=1, padx=5, pady=5)
        vcmd = (self.root.register(self._validate_size_input), '%P')
        self.entry_size.config(validate='key', validatecommand=vcmd)
        self._add_context_menu(self.entry_size)
        self.label_size_tip = ttk.Label(frame3, text="")
        self.label_size_tip.grid(row=0, column=2, padx=5, pady=5)

        frame4 = ttk.Frame(self.root, padding="10")
        frame4.pack(fill=tk.X)
        self.label_method = ttk.Label(frame4, text="")
        self.label_method.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.method_combobox = ttk.Combobox(
            frame4,
            state="readonly",
            width=12
        )
        self.method_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.method_combobox.bind("<<ComboboxSelected>>", self._on_method_select)

        frame5 = ttk.Frame(self.root, padding="10")
        frame5.pack(fill=tk.X, pady=10)
        self.btn_start = ttk.Button(frame5, text="", command=self._run_generator, width=10)
        self.btn_start.grid(row=0, column=0, padx=10, pady=5)
        self.label_status = ttk.Label(frame5, text="", foreground="black")
        self.label_status.grid(row=0, column=1, padx=10, pady=5)
        self.progress = ttk.Progressbar(frame5, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress.grid(row=0, column=2, padx=10, pady=5)
        self.label_progress = ttk.Label(frame5, text="0%", foreground="#666666", width=5)
        self.label_progress.grid(row=0, column=3, padx=5, pady=5)
        self.btn_cancel = ttk.Button(frame5, text="", command=self._cancel_task, state=tk.DISABLED, width=8)
        self.btn_cancel.grid(row=0, column=4, padx=10, pady=5)

        frame6 = ttk.Frame(self.root, padding="10")
        frame6.pack(side=tk.BOTTOM, fill=tk.X)
        separator = ttk.Separator(frame6, orient='horizontal')
        separator.pack(fill=tk.X, pady=5)
        info_label = ttk.Label(
            frame6,
            text="ZipBloat © Geekline | 官网: geekline.pages.dev",
            foreground="#666666",
            font=("Arial", 9)
        )
        info_label.pack(anchor=tk.CENTER)

    def _update_lang(self, event=None):
        display_lang = self.lang_combobox.get()
        if display_lang == "中文":
            lang = "zh"
        else:
            lang = "en"
        self.language.set(lang)
        texts = self.lang_texts[lang]

        self.root.title(texts["title"])
        self.label_original.config(text=texts["original_file"])
        self.label_output.config(text=texts["output_file"])
        self.btn_browse_original.config(text=texts["browse"])
        self.btn_browse_output.config(text=texts["browse"])
        self.label_size.config(text=texts["target_size"])
        self.label_size_tip.config(text=texts["size_tip"])
        self.label_method.config(text=texts["zoom_method"])
        self.method_combobox['values'] = [texts["empty_block"], texts["nest_zip"], texts["append_junk"], texts["zip_bomb"]]
        current_method = self.zoom_method.get()
        if current_method == "empty_block":
            self.method_combobox.set(texts["empty_block"])
        elif current_method == "nest_zip":
            self.method_combobox.set(texts["nest_zip"])
        elif current_method == "append_junk":
            self.method_combobox.set(texts["append_junk"])
        else:
            self.method_combobox.set(texts["zip_bomb"])
        self.btn_start.config(text=texts["start"])
        self.btn_cancel.config(text=texts["cancel"])
        self.btn_help.config(text=texts["help_btn"])
        self.label_status.config(text=texts["status_ready"])

        self.logger.info(f"Language switched to: {lang}")

    def _on_method_select(self, event):
        display_text = self.method_combobox.get()
        lang = self.language.get()
        texts = self.lang_texts[lang]
        method_mapping = {
            texts["empty_block"]: "empty_block",
            texts["nest_zip"]: "nest_zip",
            texts["append_junk"]: "append_junk",
            texts["zip_bomb"]: "zip_bomb"
        }
        self.zoom_method.set(method_mapping[display_text])

    def _validate_size_input(self, new_value):
        if new_value == "":
            return True
        try:
            value = float(new_value)
            return 0 <= value <= 100
        except ValueError:
            return False

    def _add_context_menu(self, entry):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="全选", command=lambda: entry.select_range(0, tk.END))
        menu.add_command(label="复制", command=lambda: entry.event_generate("<<Copy>>"))
        menu.add_command(label="粘贴", command=lambda: entry.event_generate("<<Paste>>"))
        menu.add_command(label="剪切", command=lambda: entry.event_generate("<<Cut>>"))
        menu.add_separator()
        menu.add_command(label="清除", command=lambda: entry.delete(0, tk.END))
        
        def show_menu(event):
            menu.post(event.x_root, event.y_root)
        
        entry.bind("<Button-3>", show_menu)
        entry.bind("<Control-a>", lambda e: entry.select_range(0, tk.END))

    def _select_original_zip(self):
        lang = self.language.get()
        texts = self.lang_texts[lang]
        file_path = filedialog.askopenfilename(
            title=texts["original_file"],
            filetypes=[("ZIP文件", "*.zip"), ("所有文件", "*.*")]
        )
        if file_path:
            self.original_zip_path.set(file_path)
            dir_name, file_name = os.path.split(file_path)
            name, ext = os.path.splitext(file_name)
            self.output_zip_path.set(os.path.join(dir_name, f"{name}_big{ext}"))
            self.logger.info(f"Selected original file: {file_path}")

    def _select_output_zip(self):
        lang = self.language.get()
        texts = self.lang_texts[lang]
        file_path = filedialog.asksaveasfilename(
            title=texts["output_file"],
            defaultextension=".zip",
            filetypes=[("ZIP文件", "*.zip"), ("所有文件", "*.*")]
        )
        if file_path:
            self.output_zip_path.set(file_path)
            self.logger.info(f"Selected output file: {file_path}")

    def _load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_path):
            config.read(self.config_path, encoding="utf-8")
            try:
                self.original_zip_path.set(config.get("DEFAULT", "original_path", fallback=""))
                self.output_zip_path.set(config.get("DEFAULT", "output_path", fallback=""))
                self.target_size_gb.set(float(config.get("DEFAULT", "target_size", fallback=1.0)))
                self.zoom_method.set(config.get("DEFAULT", "zoom_method", fallback="empty_block"))
                self.language.set(config.get("DEFAULT", "language", fallback="zh"))
            except:
                self.target_size_gb.set(1.0)
                self.zoom_method.set("empty_block")
                self.language.set("zh")
        else:
            self.target_size_gb.set(1.0)
            self.language.set("zh")

    def _save_config(self):
        config = configparser.ConfigParser()
        config["DEFAULT"] = {
            "original_path": self.original_zip_path.get(),
            "output_path": self.output_zip_path.get(),
            "target_size": self.target_size_gb.get(),
            "zoom_method": self.zoom_method.get(),
            "language": self.language.get()
        }
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                config.write(f)
            self.logger.info("Config saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save config: {str(e)}")

    def _check_disk_space(self, path, required_gb):
        try:
            if os.name == 'nt':
                free_bytes = shutil.disk_usage(path).free
            else:
                statvfs = os.statvfs(path)
                free_bytes = statvfs.f_frsize * statvfs.f_bavail
            free_gb = free_bytes / (1024 ** 3)
            return free_gb >= required_gb * 1.1
        except Exception as e:
            self.logger.error(f"Disk space check failed: {str(e)}")
            return False

    def _check_write_permission(self, path):
        try:
            test_file = os.path.join(os.path.dirname(path), "zipbloat_test.tmp")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            return True
        except Exception as e:
            self.logger.error(f"Permission check failed: {str(e)}")
            return False

    def _cancel_task(self):
        self.is_running = False
        lang = self.language.get()
        texts = self.lang_texts[lang]
        self.label_status.config(text=texts["status_canceled"], foreground="orange")
        self.btn_start.config(state=tk.NORMAL)
        self.btn_cancel.config(state=tk.DISABLED)
        self.progress.config(value=0)
        self.label_progress.config(text="0%")
        self.logger.info("Task canceled by user")

    def _run_generator(self):
        current_time = time.time() * 1000
        if current_time - self.last_click_time < self.click_debounce_delay:
            return
        self.last_click_time = current_time
        
        if self.is_running:
            lang = self.language.get()
            texts = self.lang_texts[lang]
            messagebox.showwarning(texts["warn_running"], texts["warn_running_msg"])
            return

        original_path = self.original_zip_path.get().strip()
        output_path = self.output_zip_path.get().strip()
        lang = self.language.get()
        texts = self.lang_texts[lang]

        try:
            target_gb = float(self.target_size_gb.get())
        except ValueError:
            messagebox.showerror(texts["err_num"], texts["err_num_msg"])
            return

        if not original_path or not os.path.exists(original_path):
            messagebox.showerror(texts["err_num"], texts["err_file_not_exist"])
            self.logger.error(f"Original file not found: {original_path}")
            return

        if not original_path.lower().endswith(".zip"):
            messagebox.showerror(texts["err_num"], texts["err_file_format"])
            self.logger.error(f"Invalid file format: {original_path}")
            return

        if not output_path:
            messagebox.showerror(texts["err_num"], texts["err_output_path"])
            return

        if target_gb <= 0 or target_gb > 100:
            messagebox.showerror(texts["err_num"], texts["err_param"])
            return

        if not self._check_write_permission(output_path):
            messagebox.showerror(texts["err_num"], texts["err_permission"])
            self.logger.error(f"No write permission: {output_path}")
            return

        if not self._check_disk_space(os.path.dirname(output_path), target_gb):
            if not messagebox.askyesno(texts["warn_disk_space"], texts["warn_disk_space_msg"]):
                return

        self.is_running = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_cancel.config(state=tk.NORMAL)
        self.label_status.config(text=texts["status_running"], foreground="blue")
        self.progress.config(value=0)
        self.label_progress.config(text="0%")

        self._save_config()

        self.logger.info(
            f"Start generating - Original: {original_path}, Output: {output_path}, Target: {target_gb}GB, Method: {self.zoom_method.get()}")

        thread = threading.Thread(
            target=self._generate_big_zip,
            args=(original_path, output_path, target_gb),
            daemon=True
        )
        thread.start()

    def _generate_empty_block(self, zf, target_gb, original_path):
        chunk = b'\x00' * 1024 * 1024
        total_chunks = int(target_gb * 1024)
        zf.write(original_path, arcname=os.path.basename(original_path))
        for i in range(total_chunks):
            if not self.is_running:
                break
            zf.writestr(f'dummy_{i:06d}.bin', chunk)
            progress_value = (i + 1) / total_chunks * 100
            self.root.after(0, lambda v=progress_value: self.progress.config(value=v))
            self.root.after(0, lambda v=progress_value: self.label_progress.config(text=f"{v:.1f}%"))
        return self.is_running

    def _generate_nest_zip(self, zf, target_gb, original_path):
        original_size = os.path.getsize(original_path) / (1024 ** 3)
        nest_times = int(target_gb / original_size) if original_size > 0 else 10
        nest_times = max(1, min(nest_times, 1000))

        temp_files = []
        current_file = original_path
        for i in range(nest_times):
            if not self.is_running:
                break
            temp_zip = f"temp_nest_{i}.zip"
            with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_STORED) as temp_zf:
                temp_zf.write(current_file, arcname=os.path.basename(current_file))
            temp_files.append(temp_zip)
            current_file = temp_zip
            progress_value = (i + 1) / nest_times * 100
            self.root.after(0, lambda v=progress_value: self.progress.config(value=v))
            self.root.after(0, lambda v=progress_value: self.label_progress.config(text=f"{v:.1f}%"))

        if self.is_running:
            zf.write(current_file, arcname="nested_zip.zip")

        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
        return self.is_running

    def _generate_append_junk(self, original_path, output_path, target_gb):
        shutil.copy2(original_path, output_path)
        junk_size = int(target_gb * 1024 * 1024 * 1024)
        chunk_size = 1024 * 1024
        total_chunks = junk_size // chunk_size

        with open(output_path, 'ab') as f:
            for i in range(total_chunks):
                if not self.is_running:
                    break
                f.write(b'\x00' * chunk_size)
                progress_value = (i + 1) / total_chunks * 100
                self.root.after(0, lambda v=progress_value: self.progress.config(value=v))
                self.root.after(0, lambda v=progress_value: self.label_progress.config(text=f"{v:.1f}%"))
        
        return self.is_running

    def _generate_zip_bomb(self, zf, target_gb, original_path):
        import tempfile
        import shutil
        
        temp_dir = tempfile.mkdtemp()
        try:
            bomb_size = 1024 * 1024 * 1024
            bomb_data = b'\x00' * bomb_size
            
            bomb_layer = os.path.join(temp_dir, "bomb_layer.zip")
            with zipfile.ZipFile(bomb_layer, 'w', zipfile.ZIP_DEFLATED) as temp_zf:
                temp_zf.writestr("bomb.txt", bomb_data)
            
            layers = 5
            current_file = bomb_layer
            
            for i in range(layers):
                if not self.is_running:
                    break
                nested_zip = os.path.join(temp_dir, f"bomb_nested_{i}.zip")
                with zipfile.ZipFile(nested_zip, 'w', zipfile.ZIP_DEFLATED) as temp_zf:
                    temp_zf.write(current_file, arcname=f"layer_{i}.zip")
                if i > 0:
                    os.remove(current_file)
                current_file = nested_zip
                progress_value = (i + 1) / layers * 100
                self.root.after(0, lambda v=progress_value: self.progress.config(value=v))
                self.root.after(0, lambda v=progress_value: self.label_progress.config(text=f"{v:.1f}%"))
            
            if self.is_running:
                zf.write(current_file, arcname="zip_bomb.zip")
            
        finally:
            shutil.rmtree(temp_dir)
        
        return self.is_running

    def _generate_big_zip(self, original_path, output_path, target_gb):
        try:
            method = self.zoom_method.get()
            
            if method == "append_junk":
                success = self._generate_append_junk(original_path, output_path, target_gb)
                if self.is_running and success:
                    self.root.after(0, lambda: self._on_complete(True, output_path))
                    self.logger.info(f"Generation success: {output_path}")
                else:
                    self.root.after(0, self._clean_canceled_file, output_path)
                    self.logger.info("Generation canceled")
                return

            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
                success = False

                if method == "empty_block":
                    success = self._generate_empty_block(zf, target_gb, original_path)
                elif method == "nest_zip":
                    success = self._generate_nest_zip(zf, target_gb, original_path)
                elif method == "zip_bomb":
                    success = self._generate_zip_bomb(zf, target_gb, original_path)

            if self.is_running and success:
                self.root.after(0, lambda: self._on_complete(True, output_path))
                self.logger.info(f"Generation success: {output_path}")
            else:
                self.root.after(0, self._clean_canceled_file, output_path)
                self.logger.info("Generation canceled")
        except PermissionError:
            self.root.after(0,
                            lambda: self._on_complete(False, self.lang_texts[self.language.get()]["err_perm_detail"]))
            self.logger.error(f"Permission error: {output_path}")
        except zipfile.BadZipFile:
            self.root.after(0, lambda: self._on_complete(False, self.lang_texts[self.language.get()]["err_zip_format"]))
            self.logger.error(f"Bad ZIP file: {original_path}")
        except OSError as e:
            if "no space left" in str(e).lower() or "磁盘空间" in str(e):
                self.root.after(0,
                                lambda: self._on_complete(False, self.lang_texts[self.language.get()]["err_disk_full"]))
                self.logger.error(f"Disk full error: {str(e)}")
            else:
                self.root.after(0, lambda: self._on_complete(False,
                                                             f"{self.lang_texts[self.language.get()]['err_system']}{str(e)}"))
                self.logger.error(f"OS error: {str(e)}")
        except Exception as e:
            self.root.after(0, lambda: self._on_complete(False,
                                                         f"{self.lang_texts[self.language.get()]['err_unknown']}{str(e)}"))
            self.logger.error(f"Unknown error: {str(e)}")

    def _clean_canceled_file(self, output_path):
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except Exception as e:
                self.logger.error(f"Failed to clean canceled file: {str(e)}")
        self.progress.config(value=0)
        self.label_progress.config(text="0%")

    def _show_help(self):
        lang = self.language.get()
        texts = self.lang_texts[lang]
        messagebox.showinfo(texts["help_title"], texts["help_content"])

    def _on_complete(self, success, msg):
        self.is_running = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_cancel.config(state=tk.DISABLED)
        lang = self.language.get()
        texts = self.lang_texts[lang]

        if success:
            self.label_status.config(text=texts["status_completed"], foreground="green")
            self.progress.config(value=100)
            self.label_progress.config(text="100%")
            messagebox.showinfo(texts["success_title"], f"{texts['success_msg']}{msg}")
        else:
            self.label_status.config(text=texts["status_failed"], foreground="red")
            self.progress.config(value=0)
            self.label_progress.config(text="0%")
            messagebox.showerror(texts["fail_title"], f"{texts['fail_msg']}{msg}")


if __name__ == "__main__":
    root = tk.Tk()
    
    try:
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        else:
            icon_path = 'icon.ico'
        
        if sys.platform == 'win32':
            import ctypes
            myappid = 'geekline.zipbloat.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            root.iconbitmap(icon_path)
        else:
            root.iconbitmap(icon_path)
    except:
        pass
    
    app = ZipBloatGUI(root)

    lang = app.language.get()
    texts = app.lang_texts[lang]
    print("=" * 50)
    print(texts["console_title"])
    print(texts["console_author"])
    print(texts["console_website"])
    print("=" * 50)

    root.mainloop()