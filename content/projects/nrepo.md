+++
title = "nrepo: Convert Code to LLM prompts"
date = 2023-06-15
weight = 1
template = "project-page.html"

[taxonomies]
authors = ["M. Elashri"]

[extra]
category = "tools"
status = "Active"
technologies = ["Javescript", "HTML", "CSS"]
links = [
    { name = "GitHub Repository", url = "https://github.com/MohamedElashri/nrepo", external = true },
    { name = "Production Website", url = "https://melashri.net/nrepo", external = true }
]
+++


A web-based tool that converts code files/folders or GitHub/Gitlab repositories into structured prompts for Large Language Models (LLMs), making it easier for developers to generate context-aware prompts for code-related tasks.

## Usage

Using `nrepo` is straightforward:

1. Select your target LLM model and its token limit
2. Choose whether to strip comments from code files
3. Configure ignore patterns or use existing .gitignore rules
4. Drag and drop your files/folders or use the file selector
5. Review the processed output and copy to clipboard

There is also GitHub integration to automatically clone repositories and process them with the same options as above.

## Features

- **Multi-Model Support**: Compatible with various LLMs, to help with token limits
- **Comment Stripping**: Option to remove comments from code files for cleaner prompts
- **Ignore Patterns**: Customizable ignore patterns to exclude unnecessary files
