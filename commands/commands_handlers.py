from messages.common.common_msgs import start_message, help_message
from utils import get_user_processor


def handle_start(data):
    get_user_processor(data)
    chat_id = data["message"]["chat"]["id"]
    start_message(chat_id)


def handle_help(data):
    get_user_processor(data)
    chat_id = data["message"]["chat"]["id"]
    help_message(chat_id)


def handle_set_profile(data):
    processor = get_user_processor(data)
    processor.start_profile_flow()


def handle_find(data):
    processor = get_user_processor(data)
    processor.get_pirate()


def handle_shuffle(data):
    processor = get_user_processor(data)
    processor.shuffle()


def handle_match(data):
    processor = get_user_processor(data)
    processor.match()


def handle_cancel(data):
    processor = get_user_processor(data)
    processor.cancel()


def handle_view_profile(data):
    processor = get_user_processor(data)
    processor.view_profile()


def handle_delete(data):
    processor = get_user_processor(data)
    processor.delete_profile()


commands = {
    "/help": handle_help,
    "/start": handle_start,
    "/setprofile": handle_set_profile,
    "/find": handle_find,
    "/shuffle": handle_shuffle,
    "/sendcontact": handle_match,
    "/cancel": handle_cancel,
    "/viewprofile": handle_view_profile,
    "/deleteprofile": handle_delete,
}
