"""
메인 윈도우 (Main Window)

앱의 최상위 윈도우입니다.
로그인 성공 후 이 화면으로 전환됩니다.

구조:
- 좌측: Navbar (메뉴)
- 우측: QStackedWidget (페이지 컨테이너 — 메뉴 선택에 따라 페이지 전환)

비개발자를 위한 설명:
- QMainWindow: 앱의 "껍데기" — 제목 표시줄, 메뉴, 상태 표시줄 등을 가진 창
- QStackedWidget: 카드 덱처럼 여러 페이지를 쌓아놓고 하나만 보여주는 컨테이너
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QLabel, QPushButton, QStatusBar,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from app.ui.navbar import Navbar
from app.core.config import APP_NAME, APP_VERSION
from app.core.auth import CurrentUser
from app.core.logger import logger


class MainWindow(QMainWindow):
    """
    앱의 메인 윈도우

    로그인 후 표시되며, Navbar와 페이지 컨테이너로 구성됩니다.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """UI를 초기화합니다."""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(1024, 700)

        # --- 중앙 위젯 ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 레이아웃: 좌측(Navbar) + 우측(페이지)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- 좌측: 네비게이션 바 ---
        self.navbar = Navbar()
        main_layout.addWidget(self.navbar)

        # --- 우측: 컨텐츠 영역 ---
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # 상단 헤더 바
        self.header = self._create_header()
        content_layout.addWidget(self.header)

        # 페이지 컨테이너
        self.page_stack = QStackedWidget()
        content_layout.addWidget(self.page_stack)

        main_layout.addLayout(content_layout)

        # Navbar 시그널 연결: 메뉴 선택 → 페이지 전환
        self.navbar.page_changed.connect(self.page_stack.setCurrentIndex)

        # --- 기본 페이지 추가 ---
        self._add_default_pages()

        # --- 상태 표시줄 ---
        status_bar = QStatusBar()
        status_bar.showMessage(f"{APP_NAME} v{APP_VERSION} | 준비됨")
        self.setStatusBar(status_bar)

        logger.info("메인 윈도우 초기화 완료")

    def _create_header(self) -> QWidget:
        """상단 헤더 바를 생성합니다."""
        header = QWidget()
        header.setObjectName("header")
        header.setFixedHeight(50)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 0, 16, 0)

        # 페이지 제목
        self.page_title = QLabel("대시보드")
        self.page_title.setFont(QFont("맑은 고딕", 14))
        layout.addWidget(self.page_title)

        layout.addStretch()

        # 사용자 정보
        current_user = CurrentUser()
        if current_user.is_logged_in:
            user_label = QLabel(f"{current_user.user.username}")
            user_label.setObjectName("userLabel")
            layout.addWidget(user_label)

            role_label = QLabel(f"({current_user.user.role.name})")
            role_label.setObjectName("roleLabel")
            layout.addWidget(role_label)

        # 로그아웃 버튼
        logout_btn = QPushButton("로그아웃")
        logout_btn.setObjectName("logoutButton")
        logout_btn.setCursor(Qt.PointingHandCursor)
        # 로그아웃 시그널은 앱 레벨에서 연결합니다
        self.logout_btn = logout_btn
        layout.addWidget(logout_btn)

        return header

    def _add_default_pages(self):
        """기본 페이지들을 추가합니다."""
        # 대시보드 페이지 (예시)
        dashboard = self._create_placeholder_page(
            "대시보드",
            "환영합니다! 이곳은 대시보드 페이지입니다.\n\n"
            "이 보일러플레이트를 확장하여 원하는 기능을 추가하세요."
        )
        self.add_page("대시보드", dashboard)

    def add_page(self, title: str, widget: QWidget, icon_text: str = ""):
        """
        새 페이지를 추가합니다.

        Args:
            title: 페이지 제목 (Navbar 메뉴에도 표시)
            widget: 페이지 위젯
            icon_text: Navbar 접힘 시 표시할 짧은 텍스트
        """
        self.page_stack.addWidget(widget)
        self.navbar.add_menu(title, icon_text)

    def _create_placeholder_page(self, title: str, description: str) -> QWidget:
        """플레이스홀더(임시) 페이지를 생성합니다."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setFont(QFont("맑은 고딕", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setFont(QFont("맑은 고딕", 12))
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        return page
