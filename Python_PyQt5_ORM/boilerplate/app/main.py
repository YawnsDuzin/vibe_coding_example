"""
앱 진입점 (Application Entry Point)

이 파일이 앱의 시작점입니다.
python -m app.main 또는 python app/main.py 로 실행합니다.

실행 흐름:
1. DB 초기화 (테이블 생성, 기본 역할 설정)
2. 로그인 화면 표시
3. 로그인 성공 → 메인 윈도우 전환
4. 로그아웃 → 다시 로그인 화면
"""
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가 (패키지 임포트를 위해)
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtCore import Qt

from app.core.config import APP_NAME
from app.core.database import init_db, get_session
from app.core.logger import logger
from app.core.auth import CurrentUser
from app.repositories.user_repository import RoleRepository
from app.ui.login_form import LoginForm
from app.ui.main_window import MainWindow


class App:
    """
    앱 전체를 관리하는 클래스

    로그인 화면과 메인 윈도우 사이의 전환을 담당합니다.
    """

    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        self.qt_app.setApplicationName(APP_NAME)

        # 스타일시트 로드 (있으면)
        self._load_stylesheet()

        # --- 화면 전환용 스택 ---
        self.root = QStackedWidget()
        self.root.setWindowTitle(APP_NAME)
        self.root.setMinimumSize(1024, 700)

        # 로그인 화면
        self.login_form = LoginForm()
        self.login_form.login_success.connect(self._on_login_success)
        self.root.addWidget(self.login_form)

        # 메인 윈도우는 로그인 성공 후 생성
        self.main_window = None

    def _load_stylesheet(self):
        """QSS 스타일시트를 로드합니다."""
        style_path = project_root / "app" / "resources" / "styles" / "light.qss"
        if style_path.exists():
            with open(style_path, "r", encoding="utf-8") as f:
                self.qt_app.setStyleSheet(f.read())
            logger.info("스타일시트 로드: %s", style_path.name)

    def _on_login_success(self, user):
        """로그인 성공 시 메인 윈도우로 전환"""
        logger.info("메인 윈도우 전환: %s", user.username)

        # 기존 메인 윈도우가 있으면 제거
        if self.main_window:
            self.root.removeWidget(self.main_window)
            self.main_window.deleteLater()

        # 새 메인 윈도우 생성
        self.main_window = MainWindow()
        self.main_window.logout_btn.clicked.connect(self._on_logout)
        self.root.addWidget(self.main_window)
        self.root.setCurrentWidget(self.main_window)

    def _on_logout(self):
        """로그아웃 시 로그인 화면으로 전환"""
        CurrentUser().logout()
        self.root.setCurrentWidget(self.login_form)
        logger.info("로그인 화면으로 전환")

    def run(self) -> int:
        """앱을 실행합니다."""
        logger.info("=== %s 시작 ===", APP_NAME)

        # DB 초기화
        init_db()
        logger.info("데이터베이스 초기화 완료")

        # 기본 역할(admin, manager, user) 생성
        session = get_session()
        try:
            role_repo = RoleRepository(session)
            role_repo.ensure_default_roles()
        finally:
            session.close()

        # 앱 실행
        self.root.show()
        exit_code = self.qt_app.exec_()

        logger.info("=== %s 종료 (코드: %d) ===", APP_NAME, exit_code)
        return exit_code


def main():
    """앱의 메인 함수"""
    app = App()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
