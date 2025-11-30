import datetime
from google.adk.tools import FunctionTool
from google.adk.tools import AgentTool
from google.adk.agents import LlmAgent
from google.adk.agents import SequentialAgent

from .config import config

from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel, Field 
from google.adk.tools.tool_context import ToolContext

from .tools import analyze_codebase, save_blog_post_to_file

def get_session_state(session_search: str, tool_context: ToolContext):
    session_search='blog_post' 
    
    # Initialize recent_searches if it doesn't exist
    if "recent_searches" not in tool_context.state:
        tool_context.state["recent_searches"] = []
        
    recent_searches = tool_context.state["recent_searches"]
    if session_search not in recent_searches:
        recent_searches.append(session_search)
        tool_context.state["recent_searches"] = recent_searches
    
    return {"status": "success"}

#------------ 1. blog planner agent --------------
from google.adk.agents import LoopAgent
from google.adk.tools import google_search

from .config import config
from .agent_utils import suppress_output_callback
from .validation_checkers import OutlineValidationChecker

blog_planner = LlmAgent(
    model=config.worker_model,
    name="blog_planner",
    description="Generates a blog post outline.",
    instruction="""
    You are a technical content strategist. Your job is to create a blog post outline.
    The outline should be well-structured and easy to follow.
    It should include a title, an introduction, a main body with several sections, and a conclusion.
    If a codebase is provided, the outline should include sections for code snippets and technical deep dives.
    The codebase context will be available in the `codebase_context` state key.
    Use the information in the `codebase_context` to generate a specific and accurate outline.
    Use Google Search to find relevant information and examples to support your writing.
    Your final output should be a blog post outline in Markdown format.
    """,
    tools=[google_search],
    output_key="blog_outline",
    after_agent_callback=suppress_output_callback,
    #OutlineValidationChecker(name="outline_validation_checker"),
)

#------------ 2. blog writer agent --------------
from google.adk.agents import Agent, LoopAgent
from google.adk.tools import google_search

from .config import config
from .agent_utils import suppress_output_callback
from .validation_checkers import BlogPostValidationChecker

blog_writer = LlmAgent(
    model=config.critic_model,
    name="blog_writer",
    description="Writes a technical blog post.",
    instruction="""
    You are an expert technical writer, crafting articles for a sophisticated audience similar to that of 'Towards Data Science' and 'freeCodeCamp'.
    Your task is to write a high-quality, in-depth technical blog post based on the provided outline and codebase summary.
    The article must be well-written, authoritative, and engaging for a technical audience.
    - Assume your readers are familiar with programming concepts and software development.
    - Dive deep into the technical details. Explain the 'how' and 'why' behind the code.
    - Use code snippets extensively to illustrate your points.
    - Use Google Search to find relevant information and examples to support your writing.
    - The codebase context will be available in the `codebase_context` state key.
    The final output must be a complete blog post in Markdown format. Do not wrap the output in a code block.
    """,
    tools=[google_search],
    output_key="blog_post",
    after_agent_callback=suppress_output_callback,
    #BlogPostValidationChecker(name="blog_post_validation_checker"), 
)

#------------ 3. blog editor agent --------------
from google.adk.agents import LlmAgent

from .config import config
from .agent_utils import suppress_output_callback

blog_editor = LlmAgent(
    model=config.critic_model,
    name="blog_editor",
    description="Edits a technical blog post based on user feedback.",
    instruction="""
    You are a professional technical editor. You will be given a blog post and user feedback.
    Your task is to edit the blog post based on the provided feedback.
    The final output should be a revised blog post in Markdown format.
    """,
    output_key="blog_post",
    after_agent_callback=suppress_output_callback,
)
#------------ 4. social media agent --------------
from google.adk.agents import LlmAgent

from .config import config

social_media_writer = LlmAgent(
    model=config.critic_model,
    name="social_media_writer",
    description="Writes social media posts to promote the blog post.",
    instruction="""
    You are a social media marketing expert. You will be given a blog post, and your task is to write social media posts for the following platforms:
    - Twitter: A short, engaging tweet that summarizes the blog post and includes relevant hashtags.
    - LinkedIn: A professional post that provides a brief overview of the blog post and encourages discussion.

    The final output should be a markdown-formatted string with the following sections:

    ### Twitter Post

    ```
    <twitter_post_content>
    ```

    ### LinkedIn Post

    ```
    <linkedin_post_content>
    ```
    """,
    output_key="social_media_posts",
)

#-------------------- root agent -----------------------
blog_workflow = SequentialAgent(
    name='blog_workflow',
    sub_agents=[blog_planner, blog_writer, blog_editor, social_media_writer],
    description="The primary technical blogging assistant. Blog writer collaborates with the user to create a blog post.",
)
root_agent = blog_workflow 
