"""
로그인/회원가입 폼 (Login/Register Form)

앱 시작 시 가장 먼저 보이는 화면입니다.
사용자 인증 후 메인 윈도우로 전환됩니다.

비개발자를 위한 설명:
- QWidget: 화면에 보이는 모든 것의 기본 단위 (버튼, 입력칸 등)
- QVBoxLayout/QHBoxLayout: 위젯을 세로/가로로 배치하는 도구
- Signal/Slot: "이벤트가 발생하면(Signal) → 이 함수를 실행해라(Slot)" 패턴
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QStackedWidget, QMessageBox,
    QComboBox, QFrame,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from app.services.auth_service import AuthService
from app.core.exceptions import AppError
from app.core.config import APP_NAME


class LoginForm(QWidget):
    """
    로그인/회원가입 화면

    Signals:
        login_success: 로그인 성공 시 발생하는 시그널 (User 객체 전달)
    """
    # 시그널 정의: 로그인 성공 시 발생 → 메인 윈도우가 이 시그널을 받아 화면 전환
    login_success = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_service = AuthService()
        self._init_ui()

    def _init_ui(self):
        """UI 구성요소를 초기화합니다."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)

        # --- 앱 타이틀 ---
        title = QLabel(APP_NAME)
        title.setFont(QFont("맑은 고딕", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("appTitle")
        layout.addWidget(title)
        layout.addSpacing(30)

        # --- 로그인/회원가입 전환을 위한 스택 위젯 ---
        # QStackedWidget: 여러 화면을 겹쳐놓고 하나만 보여주는 컨테이너
        self.stack = QStackedWidget()
        self.stack.setMaximumWidth(400)

        # 로그인 페이지 (인덱스 0)
        self.login_page = self._create_login_page()
        self.stack.addWidget(self.login_page)

        # 회원가입 페이지 (인덱스 1)
        self.register_page = self._create_register_page()
        self.stack.addWidget(self.register_page)

        layout.addWidget(self.stack, alignment=Qt.AlignCenter)

    def _create_login_page(self) -> QWidget:
        """로그인 페이지를 생성합니다."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        # 제목
        header = QLabel("로그인")
        header.setFont(QFont("맑은 고딕", 16))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # 구분선
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layout.addWidget(line)
        layout.addSpacing(10)

        # 사용자명 입력
        layout.addWidget(QLabel("사용자명"))
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("사용자명을 입력하세요")
        layout.addWidget(self.login_username)

        # 비밀번호 입력
        layout.addWidget(QLabel("비밀번호"))
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("비밀번호를 입력하세요")
        self.login_password.setEchoMode(QLineEdit.Password)  # 입력 내용 숨김
        layout.addWidget(self.login_password)
        layout.addSpacing(10)

        # 로그인 버튼
        self.login_btn = QPushButton("로그인")
        self.login_btn.setObjectName("primaryButton")
        self.login_btn.clicked.connect(self._on_login)  # 클릭 시 _on_login 실행
        layout.addWidget(self.login_btn)

        # 회원가입 전환 링크
        switch_btn = QPushButton("계정이 없으신가요? 회원가입")
        switch_btn.setObjectName("linkButton")
        switch_btn.setFlat(True)
        switch_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(switch_btn)

        # Enter 키로 로그인
        self.login_password.returnPressed.connect(self._on_login)

        return page

    def _create_register_page(self) -> QWidget:
        """회원가입 페이지를 생성합니다."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        # 제목
        header = QLabel("회원가입")
        header.setFont(QFont("맑은 고딕", 16))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # 구분선
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layout.addWidget(line)
        layout.addSpacing(10)

        # 사용자명 입력
        layout.addWidget(QLabel("사용자명"))
        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("사용자명을 입력하세요")
        layout.addWidget(self.reg_username)

        # 이메일 입력
        layout.addWidget(QLabel("이메일"))
        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("이메일을 입력하세요")
        layout.addWidget(self.reg_email)

        # 비밀번호 입력
        layout.addWidget(QLabel("비밀번호"))
        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("비밀번호를 입력하세요")
        self.reg_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_password)

        # 비밀번호 확인
        layout.addWidget(QLabel("비밀번호 확인"))
        self.reg_password_confirm = QLineEdit()
        self.reg_password_confirm.setPlaceholderText("비밀번호를 다시 입력하세요")
        self.reg_password_confirm.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_password_confirm)

        layout.addSpacing(10)

        # 회원가입 버튼
        self.register_btn = QPushButton("회원가입")
        self.register_btn.setObjectName("primaryButton")
        self.register_btn.clicked.connect(self._on_register)
        layout.addWidget(self.register_btn)

        # 로그인 전환 링크
        switch_btn = QPushButton("이미 계정이 있으신가요? 로그인")
        switch_btn.setObjectName("linkButton")
        switch_btn.setFlat(True)
        switch_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(switch_btn)

        return page

    def _on_login(self):
        """로그인 버튼 클릭 시 실행되는 슬롯(Slot)"""
        username = self.login_username.text().strip()
        password = self.login_password.text()

        if not username or not password:
            QMessageBox.warning(self, "입력 오류", "사용자명과 비밀번호를 모두 입력하세요.")
            return

        try:
            user = self.auth_service.login(username, password)
            # 로그인 성공 시그널 발생 → 메인 윈도우가 이를 받아 화면 전환
            self.login_success.emit(user)
        except AppError as e:
            QMessageBox.warning(self, "로그인 실패", e.message)

    def _on_register(self):
        """회원가입 버튼 클릭 시 실행되는 슬롯(Slot)"""
        username = self.reg_username.text().strip()
        email = self.reg_email.text().strip()
        password = self.reg_password.text()
        password_confirm = self.reg_password_confirm.text()

        # 입력 검증
        if not all([username, email, password, password_confirm]):
            QMessageBox.warning(self, "입력 오류", "모든 항목을 입력하세요.")
            return

        if password != password_confirm:
            QMessageBox.warning(self, "입력 오류", "비밀번호가 일치하지 않습니다.")
            return

        if len(password) < 4:
            QMessageBox.warning(self, "입력 오류", "비밀번호는 4자 이상이어야 합니다.")
            return

        try:
            self.auth_service.register(username, email, password)
            QMessageBox.information(self, "성공", "회원가입이 완료되었습니다. 로그인하세요.")
            # 회원가입 성공 후 로그인 페이지로 전환
            self.stack.setCurrentIndex(0)
            self.login_username.setText(username)
        except AppError as e:
            QMessageBox.warning(self, "회원가입 실패", e.message)
