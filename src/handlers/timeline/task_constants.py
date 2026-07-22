"""Timeline task constants shared across handlers."""

# Tasks that should hide the counter UI in timeline columns.
COUNTER_HIDDEN_TASKS = (
    "休憩",
    "委員会",
    "WG活動",
    "勉強会参加",
    "1on1",
    "周術期薬剤管理準備",
    "カンファレンス",
    "業務調整",
    "管理業務",
    "金庫管理薬定数確認",
    "手術使用薬剤確認・補充",
    "ICTリンクスタッフ活動",
    "医療安全対策WG活動",
    "薬剤部連絡会",
    "薬剤使用期限確認",
    "手術室サテライト薬剤定数確認",
    "実習生対応",
    "will_accept",
)


def is_counter_hidden_task(task: str) -> bool:
    return task in COUNTER_HIDDEN_TASKS