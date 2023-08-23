"""Top-level package for Imaginary Dev OpenAI wrapper."""

__author__ = """Alec Flett"""
__email__ = "alec@thegp.com"
__version__ = "0.9.3"
from .client import event_session, send_event
from .patch import patch_openai, patched_openai
from .template import TemplateChat, TemplateString
