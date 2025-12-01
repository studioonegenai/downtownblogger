# Downtown Blogger

A multi-agent blog creation system built with Google's Agent Development Kit (ADK)

---

## Problem Statement

Writing blogs manually is time-consuming and often yields inconsistent results. The repetitive nature of structuring posts and maintaining a consistent tone across multiple articles can be mentally exhausting and drain creative energy. Manual blog writing also struggles to scale when content demands increase, forcing writers to choose between quality and quantity—or invest in hiring additional staff.

Automation can streamline research gathering, generate initial drafts, handle formatting consistency, and maintain publishing schedules. This allows human writers to focus their expertise on strategic direction, creative refinement, and adding the unique insights that truly require human judgment.

---

## Why Agents?

Agents are uniquely suited to solve this problem because they can:

- **Research automatically** — Gather information from multiple sources, synthesize key insights, and identify trending themes relevant to your target audience
- **Generate drafts intelligently** — Create initial outlines or full articles based on specific parameters like tone and length, significantly reducing the "blank page problem"
- **Manage the publishing workflow end-to-end** — Schedule posts, distribute content across platforms, monitor performance metrics, and suggest improvements based on engagement data

This transforms blog management from a manual chore into a streamlined, data-driven process.

---

## What I Created

### Architecture Overview

Based on the Google ADK starter pack `blog_writer` and Kaggle demo code snippets, this version of the blogger agent—named **Downtown Blogger**—is a prime example of a multi-agent system. Rather than a monolithic application, it's an ecosystem of specialized agents, each contributing to a different stage of the blog creation process.

This modular approach, facilitated by Google's Agent Development Kit, enables a sophisticated and robust workflow. The central orchestrator is the `blog_workflow` agent.

The sequential blogger agent is constructed using the `Agent` class from Google ADK. Its definition includes several key parameters:
- The agent name
- The model powering its reasoning capabilities
- A detailed description and instruction set governing its behavior
- The `sub_agents` it delegates tasks to
- Utilities and custom tools it leverages

### The Agent Team

A 3-agent team of sub-agents comprises the core blog creation workflow:

#### 🎯 Content Strategist: `blog_planner`
Responsible for creating a well-structured and comprehensive outline for the blog post. When a user enters a topic, the planner uses Google Search to find suitable subtopics and creates a blog outline for later refinement. The `OutlineValidationChecker` ensures the generated outline meets predefined quality standards.

#### ✍️ Technical Writer: `blog_writer`
Once the outline is approved, the session markdown is passed to the `blog_writer`. This agent is an expert technical writer capable of crafting in-depth, engaging articles for a sophisticated audience. The `BlogPostValidationChecker` ensures the quality of the written content.

#### 📝 Editor: `blog_editor`
A professional technical editor that revises the blog post based on user feedback. This enables an iterative, collaborative writing process to ensure the final article meets expectations. In this demo version, all user feedback is accepted by default.

#### 📱 Social Media Marketer: `social_media_writer`
To maximize the reach of created content, this agent generates promotional posts for platforms like Twitter and LinkedIn. It crafts engaging, platform-appropriate content designed to drive traffic to the blog post.

---

## Demo

- Screenshots attached showing the build process in ADK
- Terminal CLI deployment to Cloud Run using ADK
- Observability via logs and metrics in GCP Console
- GitHub public repo published and linked

---

## The Build

**Tools & Technologies Used:**
- Google Agent Development Kit (ADK)
- Google Cloud Run
- GCP Console (logging & metrics)

The `blog_workflow` sequential agent demonstrates how multi-agent systems built with powerful frameworks like Google's ADK can tackle complex, real-world problems. By decomposing technical content creation into a series of manageable tasks and assigning them to specialized agents, it creates a workflow that is both efficient and robust.

---

## Future Improvements

With more time, I would:

- **Add a custom web UI** — Deploy to a dedicated URL for easier access
- **Implement human-in-the-loop checkpoints** — Allow user review and approval at key stages during the sequential orchestration
- **Add long-term memory** — Extend beyond session memory to remember user preferences and past interactions for a more personalized experience
