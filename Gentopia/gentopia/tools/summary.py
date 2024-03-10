from transformers import pipeline
from typing import Any, Optional, Type
from gentopia.tools.basetool import BaseModel, BaseTool, Field

class SummaryArgs(BaseModel):
    text: str = Field(..., description="Text to summarize.")

class SummaryTool(BaseTool):
    """Tool that summarizes text."""

    name = "summary_tool"
    description = "A tool for summarizing text."
    args_schema: Optional[Type[BaseModel]] = SummaryArgs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.__dict__["_summarizer"] = pipeline("summarization")

    @property
    def summarizer(self):
        """Access the summarization pipeline."""
        return self.__dict__["_summarizer"]

    def summarize_text(self, text: str) -> str:
        """Summarizes the given text."""
        summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']

    def _run(self, text: str) -> str:
        return self.summarize_text(text)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    summary_tool = SummaryTool()

