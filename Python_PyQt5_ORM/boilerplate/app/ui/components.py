"""
공통 UI 컴포넌트 (Common Components)

앱 전체에서 재사용하는 커스텀 UI 컴포넌트들입니다.

비개발자를 위한 설명:
- ToastNotification: 화면 상단에 잠시 나타났다 사라지는 알림 메시지
- ConfirmDialog: "정말 삭제하시겠습니까?" 같은 확인/취소 팝업
- LoadingSpinner: 데이터를 불러오는 동안 표시하는 로딩 표시
- ThemeToggle: 라이트/다크 테마를 전환하는 버튼
"""
from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QDialog, QGraphicsOpacityEffect, QApplication,
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QSize
from PyQt5.QtGui import QFont, QPainter, QColor, QPen


class ToastNotification(QLabel):
    """
    토스트 알림 — 화면 상단에 잠시 표시되는 메시지

    사용 예시:
        toast = ToastNotification(parent_widget)
        toast.show_message("저장되었습니다!", duration=2000)
        toast.show_message("오류 발생!", toast_type="error")
    """

    # 토스트 타입별 색상
    COLORS = {
        "info": "#3498db",
        "success": "#27ae60",
        "warning": "#f39c12",
        "error": "#e74c3c",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(40)
        self.setFont(QFont("맑은 고딕", 12))
        self.hide()

        # 투명도 애니메이션 효과
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        # 자동 숨김 타이머
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._fade_out)

    def show_message(self, message: str, duration: int = 3000, toast_type: str = "info"):
        """
        토스트 메시지를 표시합니다.

        Args:
            message: 표시할 메시지
            duration: 표시 시간 (밀리초, 기본 3초)
            toast_type: 메시지 타입 ("info", "success", "warning", "error")
        """
        color = self.COLORS.get(toast_type, self.COLORS["info"])
        self.setStyleSheet(
            f"background-color: {color}; color: white; "
            f"border-radius: 6px; padding: 8px 16px;"
        )
        self.setText(message)

        # 부모 위젯의 상단 중앙에 배치
        if self.parent():
            parent_width = self.parent().width()
            self.setFixedWidth(min(parent_width - 40, 500))
            self.move((parent_width - self.width()) // 2, 10)

        self.opacity_effect.setOpacity(1.0)
        self.show()
        self.raise_()  # 최상위로 올림

        # duration 후 자동 숨김
        self._timer.start(duration)

    def _fade_out(self):
        """토스트를 숨깁니다."""
        self.hide()


class ConfirmDialog(QDialog):
    """
    확인/취소 모달 다이얼로그

    사용 예시:
        dialog = ConfirmDialog(
            parent=self,
            title="삭제 확인",
            message="정말 삭제하시겠습니까?\n이 작업은 되돌릴 수 없습니다.",
        )
        if dialog.exec_() == QDialog.Accepted:
            # 삭제 실행
            ...
    """

    def __init__(self, parent=None, title: str = "확인", message: str = ""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(350)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # 메시지
        msg_label = QLabel(message)
        msg_label.setFont(QFont("맑은 고딕", 12))
        msg_label.setWordWrap(True)
        msg_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(msg_label)

        # 버튼 영역
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        # 취소 버튼
        cancel_btn = QPushButton("취소")
        cancel_btn.setMinimumHeight(36)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        # 확인 버튼
        confirm_btn = QPushButton("확인")
        confirm_btn.setObjectName("primaryButton")
        confirm_btn.setMinimumHeight(36)
        confirm_btn.clicked.connect(self.accept)
        btn_layout.addWidget(confirm_btn)

        layout.addLayout(btn_layout)


class LoadingSpinner(QWidget):
    """
    로딩 스피너 — 작업 진행 중 표시하는 회전 애니메이션

    사용 예시:
        spinner = LoadingSpinner(parent_widget)
        spinner.start()   # 스피너 시작
        # ... 작업 수행 ...
        spinner.stop()    # 스피너 중지
    """

    def __init__(self, parent=None, size: int = 40, color: str = "#3498db"):
        super().__init__(parent)
        self._size = size
        self._color = QColor(color)
        self._angle = 0
        self._is_spinning = False

        self.setFixedSize(QSize(size, size))

        # 회전 타이머
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._rotate)
        self.hide()

    def start(self):
        """스피너를 시작합니다."""
        self._is_spinning = True

        # 부모 위젯의 중앙에 배치
        if self.parent():
            px = (self.parent().width() - self._size) // 2
            py = (self.parent().height() - self._size) // 2
            self.move(px, py)

        self.show()
        self.raise_()
        self._timer.start(50)  # 50ms 간격으로 회전

    def stop(self):
        """스피너를 중지합니다."""
        self._is_spinning = False
        self._timer.stop()
        self.hide()

    def _rotate(self):
        """회전 각도를 갱신합니다."""
        self._angle = (self._angle + 10) % 360
        self.update()  # 다시 그리기 요청

    def paintEvent(self, event):
        """스피너를 그립니다."""
        if not self._is_spinning:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self._size / 2, self._size / 2)
        painter.rotate(self._angle)

        # 원호(아크) 그리기
        pen = QPen(self._color, 3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        radius = self._size // 2 - 4
        from PyQt5.QtCore import QRectF
        rect = QRectF(-radius, -radius, radius * 2, radius * 2)
        painter.drawArc(rect, 0, 270 * 16)  # 270도 아크

        painter.end()


class ThemeToggle(QPushButton):
    """
    테마 전환 버튼 — 라이트/다크 모드를 토글합니다.

    사용 예시:
        toggle = ThemeToggle()
        toggle.theme_changed.connect(on_theme_change)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_dark = False
        self.setText("🌙 다크 모드")
        self.setObjectName("themeToggle")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(32)
        self.clicked.connect(self._toggle)

    def _toggle(self):
        """테마를 전환합니다."""
        self._is_dark = not self._is_dark

        if self._is_dark:
            self.setText("☀️ 라이트 모드")
            theme_file = "dark.qss"
        else:
            self.setText("🌙 다크 모드")
            theme_file = "light.qss"

        # 스타일시트 파일 로드
        style_path = (
            Path(__file__).resolve().parent.parent
            / "resources" / "styles" / theme_file
        )

        if style_path.exists():
            with open(style_path, "r", encoding="utf-8") as f:
                QApplication.instance().setStyleSheet(f.read())

    @property
    def is_dark(self) -> bool:
        """현재 다크 모드 여부"""
        return self._is_dark
