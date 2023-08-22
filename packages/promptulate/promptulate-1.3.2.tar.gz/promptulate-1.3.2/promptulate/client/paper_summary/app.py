import logging
import traceback
import warnings
from typing import List, Union, Optional, Any, Dict

from promptulate.tools.paper import PaperSummaryTool
from promptulate.agents.tool_agent.agent import ToolAgent
from promptulate.utils.logger import enable_log
from promptulate.llms.openai import ChatOpenAI
from promptulate.llms.openai.schema import OPENAI_MODELS
from promptulate.client.paper_summary.config import AppConfig
from promptulate.utils.openai_key_pool import export_openai_key_pool, OpenAIKeyPool

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

DRIVER_MAPPER = {"PaperSummaryTool": PaperSummaryTool, "ToolAgent": ToolAgent}
app_config = AppConfig(logger=logger)


def check_environment():
    try:
        import gradio
    except ImportError:
        raise ValueError(
            "Could not import gradio python package. "
            "Please install it with `pip install gradio`."
        )


class AppCallback:
    @staticmethod
    def generate_summary(prompt: str) -> (str, str):
        if not prompt:
            return "请输入你想要查询的论文或arxiv id", app_config.log_output
        try:
            llm = ChatOpenAI(model=app_config.cur_model)
            answer = app_config.cur_driver(llm=llm).run(prompt)
            return answer, app_config.log_output
        except Exception as e:
            return traceback.format_exc(), app_config.log_output

    @staticmethod
    def handle_dropdown_driver_select(selected_agent: str):
        """update driver"""
        app_config.cur_driver = DRIVER_MAPPER[selected_agent]
        return f"修改成功，当前模型为{selected_agent}"

    @staticmethod
    def handle_dropdown_model_select(selected_model: str) -> str:
        app_config.cur_model = selected_model
        return f"修改成功，当前模型为{selected_model}"

    @staticmethod
    def export_key(model: str, keys: str) -> str:
        export_openai_key_pool([{"model": model, "keys": keys}])
        return f"导入key成功，<{keys}>"

    @staticmethod
    def use_cache_key(**kwargs) -> str:
        if OpenAIKeyPool().all():
            return "使用缓存key"
        return "缓存key为空"


def run_client():
    check_environment()
    import gradio as gr

    with gr.Blocks() as app:
        gr.Markdown("<center><h1>Promptulate-Paper Agent</h1></center>")

        with gr.Row():
            status_display = gr.Markdown("初始化完成", elem_id="status_display")

        with gr.Row():
            with gr.Column(scale=1):
                with gr.Tab(label="输入区"):
                    text_project_info = gr.Textbox(
                        placeholder="输入你想要查询的论文或arxiv id",
                        show_label=False,
                        interactive=True,
                    )
                    button_summary = gr.Button("论文查询总结")
                    button_reset = gr.Button("重置")
                    button_stop = gr.Button("停止")
                    dropdown_agent_select = gr.Dropdown(
                        choices=list(DRIVER_MAPPER.keys()),
                        value="PaperSummaryTool",
                        multiselect=False,
                        label="选择模型",
                        info="选择不同的Agent或工具进行推理",
                        interactive=True,
                    )

                with gr.Tab(label="模型"):
                    dropdown_model_select = gr.Dropdown(
                        choices=OPENAI_MODELS,
                        value="gpt-3.5-turbo",
                        multiselect=False,
                        label="选择模型",
                        info="选择不同的大语言模型进行推理(推荐PaperSummaryTool)",
                        interactive=True,
                    )
                    text_keys = gr.Textbox(
                        placeholder="key1, key2, key3",
                        show_label=False,
                        interactive=True,
                    )
                    button_export_keys = gr.Button("导入key")
                    button_export_cache_keys = gr.Button("使用缓存key")
                    index_files = gr.Files(label="文件下载", type="file")

            with gr.Column(scale=2):
                with gr.Tab(label="WorkPlace"):
                    text_decision = gr.Textbox(
                        show_label=False, interactive=True, lines=30
                    )
                with gr.Tab(label="Log"):
                    text_log = gr.Textbox(show_label=False, interactive=True, lines=30)

        """event callback place"""
        dropdown_agent_select.change(
            AppCallback.handle_dropdown_driver_select,
            inputs=[dropdown_agent_select],
            outputs=[status_display],
        )
        dropdown_model_select.change(
            AppCallback.handle_dropdown_model_select,
            inputs=[dropdown_model_select],
            outputs=[status_display],
        )

        button_summary.click(
            AppCallback.generate_summary,
            inputs=[text_project_info],
            outputs=[text_decision, text_log],
        )

        button_export_keys.click(
            AppCallback.export_key,
            inputs=[dropdown_model_select, text_keys],
            outputs=[status_display],
        )

        button_export_cache_keys.click(
            AppCallback.use_cache_key, outputs=[status_display]
        )

    try:
        app.launch()
    except Exception as e:
        app.show_error(e)


def main():
    enable_log()
    # run_client()
    paper_summary_tool = PaperSummaryTool()
    result = paper_summary_tool.run("2305.01555")
    print(result)


if __name__ == "__main__":
    main()
