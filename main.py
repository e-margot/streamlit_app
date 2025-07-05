import streamlit as st
import os

FILE_NAME = "/Users/margaritaermacenkova/Documents/jupyter-prototype/generator/prompts.py"



def load_prompts(file_name):
    """Загрузить значения из prompts.py"""
    prompts = {
        "SYSTEM_PROMPT": 'не удалось подключиться к файлу',
        "BOT_GENERATION_SYSTEM_PROMPT": 'не удалось подключиться к файлу',
        "PARAMETERS": ["не удалось подключиться к файлу"]
    }
    print(os.path.isfile(file_name))
    if not os.path.isfile(file_name):
        return prompts

    local_vars = {}
    with open(file_name, "r", encoding="utf-8") as f:
        code = f.read()
        try:
            exec(code, {}, local_vars)
        except Exception:
            return prompts
    prompts["SYSTEM_PROMPT"] = local_vars.get("SYSTEM_PROMPT", prompts["SYSTEM_PROMPT"])
    prompts["BOT_GENERATION_SYSTEM_PROMPT"] = local_vars.get("BOT_GENERATION_SYSTEM_PROMPT", prompts["BOT_GENERATION_SYSTEM_PROMPT"])
    prompts["PARAMETERS"] = local_vars.get("PARAMETERS", prompts["PARAMETERS"])
    return prompts

def save_prompts(file_name, f_prompt, str_prompt, list_prompt):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(f'SYSTEM_PROMPT = """{f_prompt}"""\n\n')
        f.write(f'BOT_GENERATION_SYSTEM_PROMPT = """{str_prompt}"""\n\n')
        f.write("PARAMETERS = [\n")
        for item in list_prompt:
            f.write(f'    "{item}",\n')
        f.write("]\n")

# --- Интерфейс ---

if st.button("Обновить значения из файла"):
    st.rerun()

st.title("Редактор промптов")

# 1. Загрузить значения из файла (или дефолтные)
prompts = load_prompts(FILE_NAME)

# st.subheader("Текущие значения из файла:")
# st.code(
#     f"SYSTEM_PROMPT:\n{prompts['SYSTEM_PROMPT']}\n\n"
#     f"BOT_GENERATION_SYSTEM_PROMPT:\n{prompts['BOT_GENERATION_SYSTEM_PROMPT']}\n\n"
#     f"PARAMETERS:\n{prompts['PARAMETERS']}"
# )

st.markdown("""
    <style>
    .big-textarea textarea {
        min-height: 300px !important;
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)



if "{" in prompts["SYSTEM_PROMPT"] or "}" in prompts["SYSTEM_PROMPT"]:
    st.warning(
        "Если хотите вставить фигурные скобки в f-строку, используйте двойные: {{ и }}. "
        "Иначе возникнет ошибка при чтении файла. "
        "Если при попытке обновить страницу происходит ""не удалось подключиться к файлу"", напишите @e_margot"
    )
st.subheader("Список параметров для сбора тз")
PARAMETERS_text = st.text_area(
    "PARAMETERS (по одному элементу на строку)",
    value="\n".join(prompts["PARAMETERS"]),
    key="sys_param",
    height=250,
)
PARAMETERS = [line.strip() for line in PARAMETERS_text.splitlines() if line.strip()]


st.subheader("Cистемный промпт для сбора тз")
# SYSTEM_PROMPT = st.text_area("SYSTEM_PROMPT", value=prompts["SYSTEM_PROMPT"])
SYSTEM_PROMPT = st.text_area(
    "SYSTEM_PROMPT",
    value=prompts["SYSTEM_PROMPT"],
    key="sys_prompt_big",
    height=550,
)
# st.write("**Превью f-строки:**")
# try:
#     st.code(SYSTEM_PROMPT.format(username="Иван"), language="markdown")
# except Exception as e:
#     st.error(f"Ошибка при подстановке: {e}")

st.subheader("Системный промпт для генерации бота исходя из требований")
BOT_GENERATION_SYSTEM_PROMPT = st.text_area(
    "BOT_GENERATION_SYSTEM_PROMPT",
    value=prompts["BOT_GENERATION_SYSTEM_PROMPT"],
    key="bot_gen_prompt_big",
    height=550,
)
# st.code(BOT_GENERATION_SYSTEM_PROMPT, language="markdown")


if st.button("Сохранить"):
    save_prompts(FILE_NAME, SYSTEM_PROMPT, BOT_GENERATION_SYSTEM_PROMPT, PARAMETERS)
    st.success("Сохранено! Перезапустите страницу, чтобы увидеть обновление.")
    # if st.button("Обновить значения из файла"):
    st.rerun()
