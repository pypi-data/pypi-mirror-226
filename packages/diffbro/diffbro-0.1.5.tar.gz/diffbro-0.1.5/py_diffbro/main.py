import argparse
from py_diffbro.modules.constants import PROGRAMMING_FILE_EXTENSIONS
from py_diffbro.modules.llm import prompt
from py_diffbro.modules.git import get_git_diff
from py_diffbro.modules.app_types import BroMode
from py_diffbro.modules.bro import get_diffbro_prompt


# here's a comment to test the git diff
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--chill", action="store_true")
    parser.add_argument("-m", "--mid", action="store_true")
    parser.add_argument("-d", "--chad", action="store_true")
    parser.add_argument("-o", "--model", type=str, default="gpt-3.5-turbo")
    parser.add_argument(
        "--only",
        nargs="*",
        default=PROGRAMMING_FILE_EXTENSIONS,
    )
    parser.add_argument("--ignore", nargs="*", default=[""])
    args = parser.parse_args()

    model = args.model
    bro_mode: BroMode = BroMode.CHILL
    only = args.only
    ignore = args.ignore

    if args.mid:
        bro_mode = BroMode.MID
    elif args.chad:
        bro_mode = BroMode.CHAD

    git_diff = get_git_diff(only, ignore)

    if not git_diff:
        print(f"No git diff for diffbro")
        return

    print(
        f"Building prompt for diffbro in bromode: '{bro_mode}' mode on GPT model '{model}'"
    )

    prompt_text = get_diffbro_prompt(bro_mode, git_diff)

    print(f"Running DIFFBRO")

    response = prompt(prompt_text, model)

    print("DIFFBRO\n\n", response)


if __name__ == "__main__":
    main()
