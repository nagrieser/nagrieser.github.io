+++
title = "LHCb Finder: Semantic Search for LHCb Papers"
date = 2024-03-10
weight = 3
template = "project-page.html"

[taxonomies]
authors = ["M. Elashri"]

[extra]
category = "Software"
status = "Completed"
technologies = ["Python", "FastAPI", "sentence-transformers"]
links = [
    { name = "Github Repository", url = "https://github.com/MohamedElashri/lhcbfinder", external = true },
    { name = "Production Website", url = "https://lhcbfinder.net", icon = "text" }
]
+++

A semantic search engine for LHCb research papers, enabling researchers to quickly find relevant publications using natural language queries. The project leverages state-of-the-art NLP techniques to index and retrieve scientific documents based on their content. This is ready for public release and is currently hosted at [lhcbfinder.net](https://lhcbfinder.net).


## Key Features

- **Natural Language Search**: Users can search for papers using everyday language, making it accessible to non-experts.
- **Contextual Understanding**: The system understands the context of queries, improving the relevance of search results.
- **User-friendly Interface**: The web interface is designed for ease of use, with intuitive navigation and search capabilities.

## Implementation 

This is using `FastAPI` for backend for serving the API endpoints. The backend is responsible for handling user queries, processing them, and returning relevant search results. Mixture of `pinecone` and selfhosted embeddings are used for indexing and retrieving documents. More information about the details can be found
in the project [repository](https://github.com/MohamedElashri/lhcbfinder).


