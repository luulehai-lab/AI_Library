E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\backend\database.py:207:16
    |
205 |         match = re.search(r'\((\d+)/', book['status'])
206 |         if match:
207 |             try: total_pages_reading += int(match.group(1))
    |                ^
208 |             except (ValueError, IndexError): continue
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\backend\database.py:208:44
    |
206 |         if match:
207 |             try: total_pages_reading += int(match.group(1))
208 |             except (ValueError, IndexError): continue
    |                                            ^
209 |
210 |     conn.close()
    |

F401 [*] `PyQt6.QtCore.QSize` imported but unused
  --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:30:39
   |
28 |                              QStackedWidget, QListWidget, QListWidgetItem,
29 |                              QDialog, QFormLayout, QTextEdit, QScrollArea, QInputDialog, QMenu, QSplitter)
30 | from PyQt6.QtCore import QThread, Qt, QSize, QSettings, QTimer, QObject, pyqtSignal, QUrl
   |                                       ^^^^^
31 | from PyQt6.QtGui import QIcon, QPixmap, QAction, QDesktopServices
32 | from backend.ai_service import AIServiceWorker
   |
help: Remove unused import: `PyQt6.QtCore.QSize`

F401 [*] `PyQt6.QtGui.QIcon` imported but unused
  --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:31:25
   |
29 |                              QDialog, QFormLayout, QTextEdit, QScrollArea, QInputDialog, QMenu, QSplitter)
30 | from PyQt6.QtCore import QThread, Qt, QSize, QSettings, QTimer, QObject, pyqtSignal, QUrl
31 | from PyQt6.QtGui import QIcon, QPixmap, QAction, QDesktopServices
   |                         ^^^^^
32 | from backend.ai_service import AIServiceWorker
33 | from backend.database import (get_filtered_books, add_book, update_book_field, get_library_stats, 
   |
help: Remove unused import: `PyQt6.QtGui.QIcon`

F401 [*] `openpyxl.styles.Border` imported but unused
  --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:42:59
   |
40 | from openpyxl.drawing.image import Image as OpenpyxlImage
41 | from openpyxl.utils import get_column_letter
42 | from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
   |                                                           ^^^^^^
43 | from openpyxl.worksheet.table import Table, TableStyleInfo
   |
help: Remove unused import

F401 [*] `openpyxl.styles.Side` imported but unused
  --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:42:67
   |
40 | from openpyxl.drawing.image import Image as OpenpyxlImage
41 | from openpyxl.utils import get_column_letter
42 | from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
   |                                                                   ^^^^
43 | from openpyxl.worksheet.table import Table, TableStyleInfo
   |
help: Remove unused import

E701 Multiple statements on one line (colon)
  --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:85:35
   |
83 |                 row_data = []
84 |                 for col in self.db_columns:
85 |                     if col == 'id': continue
   |                                   ^
86 |                     # Nß║┐u l├á cß╗Öt cover_path, ta ghi chuß╗ùi rß╗ùng ─æß╗â chß╗ë hiß╗çn ß║únh
87 |                     if col == 'cover_path':
   |

F841 Local variable `cover_col_index` is assigned to but never used
  --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:94:13
   |
93 |             # 4. Ch├¿n ß║únh v├á ─Éß╗ïnh dß║íng Cell
94 |             cover_col_index = self.db_columns.index('cover_path')
   |             ^^^^^^^^^^^^^^^
95 |             # T├¼m vß╗ï tr├¡ cß╗Öt B├¼a s├ích trong Excel (1-based)
96 |             try:
   |
help: Remove assignment to unused variable `cover_col_index`

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:292:26
    |
290 |     def send_chat_message(self):
291 |         user_query = self.chat_input.text().strip()
292 |         if not user_query: return
    |                          ^
293 |
294 |         self.chat_history_view.append(f"<b>Bß║ín:</b> {user_query}")
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:329:26
    |
327 |     def add_banner_images(self):
328 |         file_paths, _ = QFileDialog.getOpenFileNames(self, "Chß╗ìn ß║únh b├¼a", "", "Image Files (*.png *.jpg *.jpeg)")
329 |         if not file_paths: return
    |                          ^
330 |
331 |         settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:353:50
    |
351 |                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
352 |                                      QMessageBox.StandardButton.No)
353 |         if reply == QMessageBox.StandardButton.No: return
    |                                                  ^
354 |
355 |         settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:360:20
    |
358 |         for path in paths_to_delete:
359 |             if os.path.exists(path):
360 |                 try: os.remove(path)
    |                    ^
361 |                 except OSError as e: self.show_error(f"Kh├┤ng thß╗â x├│a file: {e}")
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:361:36
    |
359 |             if os.path.exists(path):
360 |                 try: os.remove(path)
361 |                 except OSError as e: self.show_error(f"Kh├┤ng thß╗â x├│a file: {e}")
    |                                    ^
362 |
363 |         settings.setValue("bannerPaths", [])
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:369:30
    |
367 |         while self.banner_layout.count():
368 |             child = self.banner_layout.takeAt(0)
369 |             if child.widget(): child.widget().deleteLater()
    |                              ^
370 |
371 |         settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:430:42
    |
428 |     def on_header_clicked(self, logical_index):
429 |         db_col = self.db_columns[logical_index]
430 |         if db_col in ["id", "cover_path"]: return
    |                                          ^
431 |
432 |         if self.sort_column == db_col:
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:446:72
    |
444 |         db_col = self.db_columns[column_index]
445 |
446 |         if db_col in ["id", "cover_path", "review", "danh_gia_ca_nhan"]: return
    |                                                                        ^
447 |
448 |         menu = QMenu(self)
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:472:19
    |
470 |     def show_row_context_menu(self, pos):
471 |         row = self.table.rowAt(pos.y())
472 |         if row < 0: return
    |                   ^
473 |
474 |         menu = QMenu(self)
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:482:28
    |
480 |     def delete_selected_book(self, row):
481 |         book_id_item = self.table.item(row, self.db_columns.index('id'))
482 |         if not book_id_item: return
    |                            ^
483 |         book_id = book_id_item.data(Qt.ItemDataRole.UserRole)
484 |         book_title = self.table.item(row, self.db_columns.index('ten_sach')).text()
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:496:32
    |
495 |     def on_cell_changed(self, row, column):
496 |         if self.is_loading_data: return
    |                                ^
497 |         
498 |         db_col = self.db_columns[column]
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:499:52
    |
498 |         db_col = self.db_columns[column]
499 |         if db_col in ["id", "cover_path", "status"]: return
    |                                                    ^
500 |
501 |         book_id_item = self.table.item(row, self.db_columns.index('id'))
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:502:28
    |
501 |         book_id_item = self.table.item(row, self.db_columns.index('id'))
502 |         if not book_id_item: return
    |                            ^
503 |         
504 |         book_id = book_id_item.data(Qt.ItemDataRole.UserRole)
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:518:32
    |
516 |         elif db_col == "cover_path":
517 |             book_id_item = self.table.item(row, self.db_columns.index('id'))
518 |             if not book_id_item: return
    |                                ^
519 |             book_id = book_id_item.data(Qt.ItemDataRole.UserRole)
520 |             book = get_book_by_id(book_id)
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:530:28
    |
528 |     def show_status_menu(self, row):
529 |         book_id_item = self.table.item(row, self.db_columns.index('id'))
530 |         if not book_id_item: return
    |                            ^
531 |         book_id = book_id_item.data(Qt.ItemDataRole.UserRole)
    |

F541 [*] f-string without any placeholders
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:551:37
    |
549 |         self.table.item(row, self.db_columns.index('status')).setText(status)
550 |         embed_and_store_book(book_id)
551 |         self.status_bar.showMessage(f"─É├ú cß║¡p nhß║¡t trß║íng th├íi", 3000)
    |                                     ^^^^^^^^^^^^^^^^^^^^^^^^^
552 |         self.update_status_bar()
    |
help: Remove extraneous `f` prefix

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:654:46
    |
653 |     def start_processing(self):
654 |         if not self.upload_button.isEnabled(): return
    |                                              ^
655 |
656 |         input_dir = "images_input"
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:759:24
    |
757 |                 match = re.search(r'\((\d+)/', book['status'])
758 |                 if match:
759 |                     try: filtered_reading += int(match.group(1))
    |                        ^
760 |                     except (ValueError, IndexError): continue
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:760:52
    |
758 |                 if match:
759 |                     try: filtered_reading += int(match.group(1))
760 |                     except (ValueError, IndexError): continue
    |                                                    ^
761 |         
762 |         gt = self.grand_total_stats
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:796:27
    |
795 |         for key, value in dict(book_data).items():
796 |             if key == 'id': continue
    |                           ^
797 |             display_key = key.replace('_', ' ').title()
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:860:20
    |
858 |         settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
859 |         geometry = settings.value("geometry")
860 |         if geometry: self.restoreGeometry(geometry)
    |                    ^
861 |         
862 |         state = settings.value("windowState")
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:863:17
    |
862 |         state = settings.value("windowState")
863 |         if state: self.restoreState(state)
    |                 ^
864 |
865 |         header_state = settings.value("tableHeaderState")
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:866:24
    |
865 |         header_state = settings.value("tableHeaderState")
866 |         if header_state: self.table.horizontalHeader().restoreState(header_state)
    |                        ^
867 |         
868 |         self.load_banner_images()
    |

F841 Local variable `btn_close` is assigned to but never used
   --> Z_LUU_TRU\01_GOOD_1312\frontend\main_window.py:927:9
    |
925 |         btn_open_file = msg_box.addButton("Mß╗ƒ File", QMessageBox.ButtonRole.ActionRole)
926 |         btn_open_folder = msg_box.addButton("Mß╗ƒ Th╞░ mß╗Ñc", QMessageBox.ButtonRole.ActionRole)
927 |         btn_close = msg_box.addButton("─É├│ng", QMessageBox.ButtonRole.RejectRole)
    |         ^^^^^^^^^
928 |         
929 |         msg_box.exec()
    |
help: Remove assignment to unused variable `btn_close`

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\backend\database.py:208:16
    |
206 |         match = re.search(r'\((\d+)/', book['status'])
207 |         if match:
208 |             try: total_pages_reading += int(match.group(1))
    |                ^
209 |             except (ValueError, IndexError): continue
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\backend\database.py:209:44
    |
207 |         if match:
208 |             try: total_pages_reading += int(match.group(1))
209 |             except (ValueError, IndexError): continue
    |                                            ^
210 |
211 |     conn.close()
    |

F401 [*] `markdown` imported but unused
  --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:29:8
   |
27 | import os
28 | import shutil
29 | import markdown
   |        ^^^^^^^^
30 | import re
31 | from datetime import datetime
   |
help: Remove unused import: `markdown`

F401 [*] `openpyxl.styles.Border` imported but unused
  --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:52:59
   |
50 | from openpyxl.drawing.image import Image as OpenpyxlImage
51 | from openpyxl.utils import get_column_letter
52 | from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
   |                                                           ^^^^^^
53 | from openpyxl.worksheet.table import Table, TableStyleInfo
   |
help: Remove unused import

F401 [*] `openpyxl.styles.Side` imported but unused
  --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:52:67
   |
50 | from openpyxl.drawing.image import Image as OpenpyxlImage
51 | from openpyxl.utils import get_column_letter
52 | from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
   |                                                                   ^^^^
53 | from openpyxl.worksheet.table import Table, TableStyleInfo
   |
help: Remove unused import

E701 Multiple statements on one line (colon)
  --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:95:35
   |
93 |                 row_data = []
94 |                 for col in self.db_columns:
95 |                     if col == 'id': continue
   |                                   ^
96 |                     # Nß║┐u l├á cß╗Öt cover_path, ta ghi chuß╗ùi rß╗ùng ─æß╗â chß╗ë hiß╗çn ß║únh
97 |                     if col == 'cover_path':
   |

F841 Local variable `cover_col_index` is assigned to but never used
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:104:13
    |
103 |             # 4. Ch├¿n ß║únh v├á ─Éß╗ïnh dß║íng Cell
104 |             cover_col_index = self.db_columns.index('cover_path')
    |             ^^^^^^^^^^^^^^^
105 |             # T├¼m vß╗ï tr├¡ cß╗Öt B├¼a s├ích trong Excel (1-based)
106 |             try:
    |
help: Remove assignment to unused variable `cover_col_index`

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:343:26
    |
341 |     def add_banner_images(self):
342 |         file_paths, _ = QFileDialog.getOpenFileNames(self, "Chß╗ìn ß║únh b├¼a", "", "Image Files (*.png *.jpg *.jpeg)")
343 |         if not file_paths: return
    |                          ^
344 |
345 |         settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:367:50
    |
365 |                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
366 |                                      QMessageBox.StandardButton.No)
367 |         if reply == QMessageBox.StandardButton.No: return
    |                                                  ^
368 |
369 |         settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:374:20
    |
372 |         for path in paths_to_delete:
373 |             if os.path.exists(path):
374 |                 try: os.remove(path)
    |                    ^
375 |                 except OSError as e: self.show_error(f"Kh├┤ng thß╗â x├│a file: {e}")
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:375:36
    |
373 |             if os.path.exists(path):
374 |                 try: os.remove(path)
375 |                 except OSError as e: self.show_error(f"Kh├┤ng thß╗â x├│a file: {e}")
    |                                    ^
376 |
377 |         settings.setValue("bannerPaths", [])
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:383:30
    |
381 |         while self.banner_layout.count():
382 |             child = self.banner_layout.takeAt(0)
383 |             if child.widget(): child.widget().deleteLater()
    |                              ^
384 |
385 |         settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:407:42
    |
405 |     def on_header_clicked(self, logical_index):
406 |         db_col = self.book_table_widget.db_columns[logical_index]
407 |         if db_col in ["id", "cover_path"]: return
    |                                          ^
408 |
409 |         if self.sort_column == db_col:
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:477:46
    |
476 |     def start_processing(self):
477 |         if not self.upload_button.isEnabled(): return
    |                                              ^
478 |
479 |         input_dir = "images_input"
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:596:24
    |
594 |                 match = re.search(r'\((\d+)/', book['status'])
595 |                 if match:
596 |                     try: filtered_reading += int(match.group(1))
    |                        ^
597 |                     except (ValueError, IndexError): continue
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:597:52
    |
595 |                 if match:
596 |                     try: filtered_reading += int(match.group(1))
597 |                     except (ValueError, IndexError): continue
    |                                                    ^
598 |         
599 |         gt = self.grand_total_stats
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:633:27
    |
632 |         for key, value in dict(book_data).items():
633 |             if key == 'id': continue
    |                           ^
634 |             display_key = key.replace('_', ' ').title()
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:697:20
    |
695 |         settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
696 |         geometry = settings.value("geometry")
697 |         if geometry: self.restoreGeometry(geometry)
    |                    ^
698 |         
699 |         state = settings.value("windowState")
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:700:17
    |
699 |         state = settings.value("windowState")
700 |         if state: self.restoreState(state)
    |                 ^
701 |
702 |         header_state = settings.value("tableHeaderState")
    |

E701 Multiple statements on one line (colon)
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:703:24
    |
702 |         header_state = settings.value("tableHeaderState")
703 |         if header_state: self.book_table_widget.table.horizontalHeader().restoreState(header_state)
    |                        ^
704 |         
705 |         self.load_banner_images()
    |

F841 Local variable `btn_close` is assigned to but never used
   --> Z_LUU_TRU\02_TINHCHINH_1312\frontend\main_window.py:766:9
    |
764 |         btn_open_file = msg_box.addButton("Mß╗ƒ File", QMessageBox.ButtonRole.ActionRole)
765 |         btn_open_folder = msg_box.addButton("Mß╗ƒ Th╞░ mß╗Ñc", QMessageBox.ButtonRole.ActionRole)
766 |         btn_close = msg_box.addButton("─É├│ng", QMessageBox.ButtonRole.RejectRole)
    |         ^^^^^^^^^
767 |         
768 |         msg_box.exec()
    |
help: Remove assignment to unused variable `btn_close`

F541 [*] f-string without any placeholders
  --> _tools\reindex_all.py:65:19
   |
63 |                 metadatas=metadatas
64 |             )
65 |             print(f"  -> Xong batch.")
   |                   ^^^^^^^^^^^^^^^^^^^
66 |             
67 |             # Nghß╗ë mß╗Öt ch├║t ─æß╗â tr├ính rate limit nß║┐u cß║ºn
   |
help: Remove extraneous `f` prefix

F821 Undefined name `total_books`
  --> _tools\reindex_all.py:77:40
   |
75 |     reindex_all()
76 |     duration = time.time() - start_time
77 |     print(f"Ho├án tß║Ñt re-index to├án bß╗Ö {total_books if 'total_books' in locals() else 'th╞░ viß╗çn'} s├ích.")
   |                                        ^^^^^^^^^^^
78 |     print(f"Thß╗¥i gian thß╗▒c hiß╗çn: {duration:.2f} gi├óy.")
   |

F541 [*] f-string without any placeholders
  --> _tools\update_batch5_metadata.py:63:27
   |
61 |                 try:
62 |                     embed_and_store_book(book_id)
63 |                     print(f"    -> ─É├ú cß║¡p nhß║¡t metadata v├á re-index ChromaDB.")
   |                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
64 |                 except Exception as e:
65 |                     print(f"    -> Lß╗ùi khi re-index ChromaDB: {e}")
   |
help: Remove extraneous `f` prefix

F401 [*] `codecs` imported but unused
  --> _tools\update_batch5_metadata.py:78:16
   |
76 | if __name__ == "__main__":
77 |     if sys.platform == "win32":
78 |         import codecs
   |                ^^^^^^
79 |         sys.stdout.reconfigure(encoding='utf-8')
   |
help: Remove unused import: `codecs`

E402 Module level import not at top of file
  --> backend\ai_service.py:15:1
   |
13 | warnings.filterwarnings("ignore", category=FutureWarning, module='google.generativeai')
14 |
15 | import google.generativeai as genai
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
16 | from PyQt6.QtCore import QObject, pyqtSignal
17 | from PIL import Image
   |

E402 Module level import not at top of file
  --> backend\ai_service.py:16:1
   |
15 | import google.generativeai as genai
16 | from PyQt6.QtCore import QObject, pyqtSignal
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
17 | from PIL import Image
18 | from config import get_api_key
   |

E402 Module level import not at top of file
  --> backend\ai_service.py:17:1
   |
15 | import google.generativeai as genai
16 | from PyQt6.QtCore import QObject, pyqtSignal
17 | from PIL import Image
   | ^^^^^^^^^^^^^^^^^^^^^
18 | from config import get_api_key
   |

E402 Module level import not at top of file
  --> backend\ai_service.py:18:1
   |
16 | from PyQt6.QtCore import QObject, pyqtSignal
17 | from PIL import Image
18 | from config import get_api_key
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
19 |
20 | def normalize_data(data):
   |

E701 Multiple statements on one line (colon)
   --> backend\database.py:195:16
    |
193 |         match = re.search(r'\((\d+)/', book['status'])
194 |         if match:
195 |             try: total_pages_reading += int(match.group(1))
    |                ^
196 |             except (ValueError, IndexError): continue
    |

E701 Multiple statements on one line (colon)
   --> backend\database.py:196:44
    |
194 |         if match:
195 |             try: total_pages_reading += int(match.group(1))
196 |             except (ValueError, IndexError): continue
    |                                            ^
197 |
198 |     conn.close()
    |

E402 Module level import not at top of file
  --> backend\rag_service.py:13:1
   |
11 | warnings.filterwarnings("ignore", category=FutureWarning, module='google.generativeai')
12 |
13 | import chromadb
   | ^^^^^^^^^^^^^^^
14 | import google.generativeai as genai
15 | from PyQt6.QtCore import QObject, pyqtSignal
   |

E402 Module level import not at top of file
  --> backend\rag_service.py:14:1
   |
13 | import chromadb
14 | import google.generativeai as genai
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
15 | from PyQt6.QtCore import QObject, pyqtSignal
16 | from config import CHROMA_PATH, CHROMA_COLLECTION, get_api_key, EMBEDDING_MODEL
   |

E402 Module level import not at top of file
  --> backend\rag_service.py:15:1
   |
13 | import chromadb
14 | import google.generativeai as genai
15 | from PyQt6.QtCore import QObject, pyqtSignal
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
16 | from config import CHROMA_PATH, CHROMA_COLLECTION, get_api_key, EMBEDDING_MODEL
17 | from .database import get_db_connection, get_book_by_id
   |

E402 Module level import not at top of file
  --> backend\rag_service.py:16:1
   |
14 | import google.generativeai as genai
15 | from PyQt6.QtCore import QObject, pyqtSignal
16 | from config import CHROMA_PATH, CHROMA_COLLECTION, get_api_key, EMBEDDING_MODEL
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
17 | from .database import get_db_connection, get_book_by_id
   |

E402 Module level import not at top of file
  --> backend\rag_service.py:17:1
   |
15 | from PyQt6.QtCore import QObject, pyqtSignal
16 | from config import CHROMA_PATH, CHROMA_COLLECTION, get_api_key, EMBEDDING_MODEL
17 | from .database import get_db_connection, get_book_by_id
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
18 |
19 | # Cß║Ñu h├¼nh API key cho Google mß╗Öt lß║ºn
   |

F401 [*] `codecs` imported but unused
  --> batch_import.py:12:12
   |
10 | # Cß║Ñu h├¼nh encoding cho console ─æß╗â in ─æ╞░ß╗úc tiß║┐ng Viß╗çt tr├¬n Windows
11 | if sys.platform == "win32":
12 |     import codecs
   |            ^^^^^^
13 |     sys.stdout.reconfigure(encoding='utf-8')
   |
help: Remove unused import: `codecs`

F541 [*] f-string without any placeholders
  --> batch_import.py:94:23
   |
92 |             thumb_path = create_thumbnail(destination_path, book_id)
93 |             if thumb_path:
94 |                 print(f"    -> ─É├ú tß║ío thumbnail")
   |                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
95 |                 
96 |             # 8. Embedding v├á l╞░u v├áo ChromaDB
   |
help: Remove extraneous `f` prefix

F541 [*] f-string without any placeholders
   --> batch_import.py:98:23
    |
 96 |             # 8. Embedding v├á l╞░u v├áo ChromaDB
 97 |             try:
 98 |                 print(f"    -> ─Éang tß║ío embedding cho ChromaDB...")
    |                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 99 |                 embed_and_store_book(book_id)
100 |                 print(f"    -> Th├ánh c├┤ng!")
    |
help: Remove extraneous `f` prefix

F541 [*] f-string without any placeholders
   --> batch_import.py:100:23
    |
 98 |                 print(f"    -> ─Éang tß║ío embedding cho ChromaDB...")
 99 |                 embed_and_store_book(book_id)
100 |                 print(f"    -> Th├ánh c├┤ng!")
    |                       ^^^^^^^^^^^^^^^^^^^^^
101 |             except Exception as e:
102 |                 print(f"    -> Lß╗ùi embedding: {e}")
    |
help: Remove extraneous `f` prefix

F541 [*] f-string without any placeholders
   --> batch_import.py:108:11
    |
106 |             print(f"    Lß╗ùi khi ghi database: {e}")
107 |         
108 |     print(f"\n========================================")
    |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
109 |     print(f"Kß║╛T QUß║ó: ─É├ú nß║íp th├ánh c├┤ng {processed_count}/{total_count} cuß╗æn s├ích.")
110 |     print(f"========================================")
    |
help: Remove extraneous `f` prefix

F541 [*] f-string without any placeholders
   --> batch_import.py:110:11
    |
108 |     print(f"\n========================================")
109 |     print(f"Kß║╛T QUß║ó: ─É├ú nß║íp th├ánh c├┤ng {processed_count}/{total_count} cuß╗æn s├ích.")
110 |     print(f"========================================")
    |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
111 |
112 | if __name__ == "__main__":
    |
help: Remove extraneous `f` prefix

F401 [*] `PyQt6.QtWidgets.QHBoxLayout` imported but unused
  --> frontend\components\dashboard_widget.py:8:60
   |
 7 | from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QScrollArea, QLabel, 
 8 |                              QFrame, QDialog, QPushButton, QHBoxLayout)
   |                                                            ^^^^^^^^^^^
 9 | from PyQt6.QtCore import Qt, pyqtSignal
10 | from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
   |
help: Remove unused import: `PyQt6.QtWidgets.QHBoxLayout`

F401 [*] `markdown` imported but unused
  --> frontend\main_window.py:31:8
   |
29 | import os
30 | import shutil
31 | import markdown
   |        ^^^^^^^^
32 | import re
33 | from datetime import datetime
   |
help: Remove unused import: `markdown`

F401 [*] `openpyxl.styles.Border` imported but unused
  --> frontend\main_window.py:56:59
   |
54 | from openpyxl.drawing.image import Image as OpenpyxlImage
55 | from openpyxl.utils import get_column_letter
56 | from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
   |                                                           ^^^^^^
57 | from openpyxl.worksheet.table import Table, TableStyleInfo
   |
help: Remove unused import

F401 [*] `openpyxl.styles.Side` imported but unused
  --> frontend\main_window.py:56:67
   |
54 | from openpyxl.drawing.image import Image as OpenpyxlImage
55 | from openpyxl.utils import get_column_letter
56 | from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
   |                                                                   ^^^^
57 | from openpyxl.worksheet.table import Table, TableStyleInfo
   |
help: Remove unused import

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:99:35
    |
 97 |                 row_data = []
 98 |                 for col in self.db_columns:
 99 |                     if col == 'id': continue
    |                                   ^
100 |                     # Nß║┐u l├á cß╗Öt cover_path, ta ghi chuß╗ùi rß╗ùng ─æß╗â chß╗ë hiß╗çn ß║únh
101 |                     if col == 'cover_path':
    |

F841 Local variable `cover_col_index` is assigned to but never used
   --> frontend\main_window.py:108:13
    |
107 |             # 4. Ch├¿n ß║únh v├á ─Éß╗ïnh dß║íng Cell
108 |             cover_col_index = self.db_columns.index('cover_path')
    |             ^^^^^^^^^^^^^^^
109 |             # T├¼m vß╗ï tr├¡ cß╗Öt B├¼a s├ích trong Excel (1-based)
110 |             try:
    |
help: Remove assignment to unused variable `cover_col_index`

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:367:26
    |
365 |     def add_banner_images(self):
366 |         file_paths, _ = QFileDialog.getOpenFileNames(self, "Chß╗ìn ß║únh b├¼a", "", "Image Files (*.png *.jpg *.jpeg)")
367 |         if not file_paths: return
    |                          ^
368 |
369 |         settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:391:50
    |
389 |                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
390 |                                      QMessageBox.StandardButton.No)
391 |         if reply == QMessageBox.StandardButton.No: return
    |                                                  ^
392 |
393 |         settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:398:20
    |
396 |         for path in paths_to_delete:
397 |             if os.path.exists(path):
398 |                 try: os.remove(path)
    |                    ^
399 |                 except OSError as e: self.show_error(f"Kh├┤ng thß╗â x├│a file: {e}")
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:399:36
    |
397 |             if os.path.exists(path):
398 |                 try: os.remove(path)
399 |                 except OSError as e: self.show_error(f"Kh├┤ng thß╗â x├│a file: {e}")
    |                                    ^
400 |
401 |         settings.setValue("bannerPaths", [])
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:407:30
    |
405 |         while self.banner_layout.count():
406 |             child = self.banner_layout.takeAt(0)
407 |             if child.widget(): child.widget().deleteLater()
    |                              ^
408 |
409 |         settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:431:42
    |
429 |     def on_header_clicked(self, logical_index):
430 |         db_col = self.book_table_widget.db_columns[logical_index]
431 |         if db_col in ["id", "cover_path"]: return
    |                                          ^
432 |
433 |         if self.sort_column == db_col:
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:514:46
    |
513 |     def start_processing(self):
514 |         if not self.upload_button.isEnabled(): return
    |                                              ^
515 |
516 |         input_dir = "images_input"
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:633:24
    |
631 |                 match = re.search(r'\((\d+)/', book['status'])
632 |                 if match:
633 |                     try: filtered_reading += int(match.group(1))
    |                        ^
634 |                     except (ValueError, IndexError): continue
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:634:52
    |
632 |                 if match:
633 |                     try: filtered_reading += int(match.group(1))
634 |                     except (ValueError, IndexError): continue
    |                                                    ^
635 |         
636 |         gt = self.grand_total_stats
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:670:27
    |
669 |         for key, value in dict(book_data).items():
670 |             if key == 'id': continue
    |                           ^
671 |             display_key = key.replace('_', ' ').title()
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:734:20
    |
732 |         settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APP_NAME)
733 |         geometry = settings.value("geometry")
734 |         if geometry: self.restoreGeometry(geometry)
    |                    ^
735 |         
736 |         state = settings.value("windowState")
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:737:17
    |
736 |         state = settings.value("windowState")
737 |         if state: self.restoreState(state)
    |                 ^
738 |
739 |         header_state = settings.value("tableHeaderState")
    |

E701 Multiple statements on one line (colon)
   --> frontend\main_window.py:740:24
    |
739 |         header_state = settings.value("tableHeaderState")
740 |         if header_state: self.book_table_widget.table.horizontalHeader().restoreState(header_state)
    |                        ^
741 |         
742 |         self.load_banner_images()
    |

F841 Local variable `btn_close` is assigned to but never used
   --> frontend\main_window.py:803:9
    |
801 |         btn_open_file = msg_box.addButton("Mß╗ƒ File", QMessageBox.ButtonRole.ActionRole)
802 |         btn_open_folder = msg_box.addButton("Mß╗ƒ Th╞░ mß╗Ñc", QMessageBox.ButtonRole.ActionRole)
803 |         btn_close = msg_box.addButton("─É├│ng", QMessageBox.ButtonRole.RejectRole)
    |         ^^^^^^^^^
804 |         
805 |         msg_box.exec()
    |
help: Remove assignment to unused variable `btn_close`

Found 94 errors.
[*] 21 fixable with the `--fix` option (6 hidden fixes can be enabled with the `--unsafe-fixes` option).
