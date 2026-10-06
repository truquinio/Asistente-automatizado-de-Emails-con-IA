import importlib
import os

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("EMAIL_ACCOUNT", "test@example.com")
os.environ.setdefault("EMAIL_PASSWORD", "test-password")


def test_runtime_modules_share_valid_settings_contract():
    config_module = importlib.import_module("config")
    processor = importlib.import_module("src.real.processor")
    response_generator = importlib.import_module("src.utils.response_generator")

    assert config_module.config.PROCESSING_LIMIT == 10
    assert config_module.config.EMAIL_FOLDERS[0] == "INBOX"
    assert processor.config is config_module.config
    assert response_generator.config is config_module.config
    assert processor.process_emails.__defaults__ == (None,)


def test_fetch_uses_configured_folder_and_limit(monkeypatch):
    processor = importlib.import_module("src.real.processor")

    class FakeServer:
        def __init__(self):
            self.selected = None
            self.fetched = None

        def login(self, *_):
            return None

        def select_folder(self, folder):
            self.selected = folder

        def search(self, *_):
            return [1, 2, 3]

        def fetch(self, messages, *_):
            self.fetched = list(messages)
            return {}

        def __enter__(self):
            return self

        def __exit__(self, *_):
            return False

    server = FakeServer()
    monkeypatch.setattr(processor, "IMAPClient", lambda **_: server)
    monkeypatch.setattr(processor.config, "EMAIL_FOLDERS", ["Custom"])
    monkeypatch.setattr(processor.config, "PROCESSING_LIMIT", 2)

    instance = processor.EmailProcessor(client=object())
    assert instance.fetch_unread_emails() == []
    assert server.selected == "Custom"
    assert server.fetched == [1, 2]
