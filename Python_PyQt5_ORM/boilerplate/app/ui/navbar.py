"""
네비게이션 바 (Navigation Bar)

좌측에 위치하는 메뉴 바로, 여러 페이지(폼)를 전환하는 역할을 합니다.
접기/펼치기(expand/collapse)가 가능합니다.

비개발자를 위한 설명:
- Navbar는 웹사이트의 좌측 메뉴와 같은 역할입니다
- 각 메뉴 버튼을 클릭하면 오른쪽 영역의 페이지가 바뀝니다
- 화살표 버튼으로 메뉴를 접거나 펼칠 수 있습니다
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize


class NavButton(QPushButton):
    """네비게이션 메뉴의 개별 버튼"""

    def __init__(self, text: str, icon_text: str = "", parent=None):
        super().__init__(parent)
        self.full_text = text       # 펼쳤을 때 보이는 전체 텍스트
        self.icon_text = icon_text  # 접었을 때 보이는 짧은 텍스트 (아이콘 대용)
        self.setText(text)
        self.setObjectName("navButton")
        self.setCheckable(True)     # 토글(선택/해제) 가능
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(44)

    def set_collapsed(self, collapsed: bool):
        """접기/펼치기 상태에 따라 표시 텍스트를 변경합니다."""
        if collapsed:
            self.setText(self.icon_text)
        else:
            self.setText(self.full_text)


class Navbar(QWidget):
    """
    좌측 네비게이션 바

    Signals:
        page_changed: 메뉴 선택 시 발생 (페이지 인덱스 전달)
    """
    # 시그널: 메뉴가 선택되면 발생 → 메인 윈도우가 해당 페이지로 전환
    page_changed = pyqtSignal(int)

    # 네비게이션 바 너비 설정
    EXPANDED_WIDTH = 200   # 펼쳤을 때
    COLLAPSED_WIDTH = 50   # 접었을 때

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("navbar")
        self._is_collapsed = False
        self._buttons: list[NavButton] = []
        self._init_ui()

    def _init_ui(self):
        """UI를 초기화합니다."""
        self.setFixedWidth(self.EXPANDED_WIDTH)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(4, 8, 4, 8)
        self.layout_.setSpacing(4)

        # 접기/펼치기 토글 버튼
        self.toggle_btn = QPushButton("◀")
        self.toggle_btn.setObjectName("navToggle")
        self.toggle_btn.setFixedHeight(32)
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self._toggle_collapse)
        self.layout_.addWidget(self.toggle_btn)

        # 메뉴 버튼들이 들어갈 공간
        self.layout_.addSpacing(8)

        # 하단 여백 (메뉴 버튼을 위쪽에 모으기 위해)
        self.layout_.addStretch()

    def add_menu(self, text: str, icon_text: str = ""):
        """
        메뉴 항목을 추가합니다.

        Args:
            text: 메뉴 이름 (예: "대시보드")
            icon_text: 접었을 때 표시할 짧은 텍스트 (예: "D")
        """
        if not icon_text:
            icon_text = text[0] if text else "?"

        btn = NavButton(text, icon_text)
        index = len(self._buttons)

        # 버튼 클릭 시 해당 페이지 인덱스를 시그널로 전달
        btn.clicked.connect(lambda checked, idx=index: self._on_menu_click(idx))

        # stretch 앞에 삽입 (stretch는 마지막에 위치)
        self.layout_.insertWidget(self.layout_.count() - 1, btn)
        self._buttons.append(btn)

        # 첫 번째 메뉴는 기본 선택
        if len(self._buttons) == 1:
            btn.setChecked(True)

    def _on_menu_click(self, index: int):
        """메뉴 버튼 클릭 시 처리"""
        # 모든 버튼의 선택 상태 해제 후 클릭된 버튼만 선택
        for i, btn in enumerate(self._buttons):
            btn.setChecked(i == index)

        # 페이지 전환 시그널 발생
        self.page_changed.emit(index)

    def _toggle_collapse(self):
        """네비게이션 바 접기/펼치기"""
        self._is_collapsed = not self._is_collapsed

        if self._is_collapsed:
            self.setFixedWidth(self.COLLAPSED_WIDTH)
            self.toggle_btn.setText("▶")
        else:
            self.setFixedWidth(self.EXPANDED_WIDTH)
            self.toggle_btn.setText("◀")

        # 모든 메뉴 버튼의 텍스트 갱신
        for btn in self._buttons:
            btn.set_collapsed(self._is_collapsed)
