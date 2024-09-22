# roast-my-docs

## summary

use llms to judge the activation energy for you project, based on your docs

## setup

### dependencies

install the following dependencies and setup an environment variable for each

- weave
- openrouter
- reader

## outline

- collect
    - provide seed url to documentation
    - collect first 20 urls
    - determine if "Getting Started" or "Quickstart" is available within urls (fuzzy match)
        - if not then scrape the home page
    - scrape getting started page
- evaluate
    - structure prompt to include site data (urls and getting started) and evaluation criteria
- display
    - parse output into structured data
    - print to the command line using rich

## references

- [Open Router | W&B Weave](https://weave-docs.wandb.ai/guides/integrations/openrouter/)
- [Reader API](https://jina.ai/reader/)
- [Judgement Day Hackathon](https://wandbai.notion.site/Judgement-Day-Hackathon-107e2f5c7ef3801eb413d569b2e5ae3d)
- [OpenRouter](https://openrouter.ai/)
