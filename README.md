<p align="center">
  <h1 align="center">D.U.D.E.</h1>
  <p align="center">
    <i align="center">Digital unified detection for entomologists</i>
  </p>
</p>

<br> <br>

This app leverages Flatbug and BioClip2 to detect and identify insect species.


## Quick start

Install using Docker compose. After cloning the repo, just enter the command:

  <code>docker compose up -d</code>

The models can take several minutes to download. For faster download of the models, I recommend using a HuggingFace token (create one here: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)). First, create a .env file from the .env.example file:

  <code>cp .env.example .env</code>

Then, add your token into the .env file.

After initial configuration, the app can be accessed locally here: [http://localhost:3000/](http://localhost:3000/)

<h3>GPU acceleration</h3>

For inference to run properly, it is recommended to have an NVIDIA GPU with CUDA installed on the machine running the service. For more informations about CUDA and how to install it: [https://letmegooglethat.com/?q=cuda+installation](https://letmegooglethat.com/?q=cuda+installation)

<h3>Using</h3>

To use the app with your own photos, upload a .zip file containing all your images in PNG or JPEG format. You can also test the app with the provided test files (./Test_files).
