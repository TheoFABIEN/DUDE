This app leverages Flatbug and BioClip2 te detect and identify insect species.


## How to use

Install using Docker compose. After cloning the repo, just enter the command:

  <code>docker compose up -d</code>

For faster download of the models, I recommend using a HuggingFace token. First, create a .env file from the .env.example file:

  <code>cp .env.example .env</code>

Then, add your token into the .env file.

To create a new HuggingFace token, go here : [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)