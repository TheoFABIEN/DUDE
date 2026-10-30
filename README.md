<p align="center">
  <h1 align="center">D.U.D.E.</h1>
  <p align="center">
    <i align="center">Digital unified detection for entomologists</i>
  </p>
</p>

<br> <br>

D.U.D.E. is a self-hosted web app that combines [Flat-Bug](https://github.com/darsa-group/flat-bug) and [BioCLIP2](https://github.com/Imageomics/bioclip-2) to find insects in your photos and suggests a species for each one.

- Upload images in .zip format
- Let the algorithm detect and identify insects for you
- Edit annotations and delete false positive if needed
- Download the results using a standard annotation format


<p align="center">
  <a href="Demo_images/DUDE_demo_1.png">
    <img src="Demo_images/DUDE_demo_1.png" width="400">
  </a>
</p>

## Table of contents

- [Quick start](#quick-start)
- [GPU acceleration](#gpu-acceleration)
- [Using the app](#using-the-app)
- [Credits and citation](#credits-and-citation)

## Quick start

<i>D.U.D.E. runs in Docker, so first make sure Docker and Docker Compose are installed.</i>

**1. Clone the repository**

```bash
git clone https://github.com/TheoFABIEN/DUDE.git
cd DUDE
```
Before proceeding, if you want to use GPU capabilities for running the model (highly recommended), now is the time to take a look at the **GPU acceleration** section.

> **No GPU?** You can still use the app by relying solely on the CPU. It will be painfully slow, though.

**2. (Optional) Add a HuggingFace token**

The HuggingFace model can take several minutes to download. If you feel like you need it, you can authenticate to HuggingFace for faster downloads and reduced risk of being rate-limited. Create a token at <https://huggingface.co/settings/tokens>, then:

```bash
cp .env.example .env
```
Open the `.env` and paste your token after `HF_TOKEN=`.

**3. Install using docker compose**

If you want to use your GPU:
```
docker compose up -d
```

If you only use the CPU:
```
docker compose -f compose-cpu.yml up -d
```

**4. Wait for the models to load, then open the app**

Once the setup is complete, the app can be accessed locally here: [http://localhost:3000/](http://localhost:3000/)


## GPU acceleration

For inference to run properly, it is recommended to have an NVIDIA GPU with [CUDA](https://developer.nvidia.com/cuda-downloads) installed on the machine running the service. You will also need to install the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) which is needed to run GPU-accelerated containers.




## Using the app

You can test the app with the provided test files: `Test_files/Test_solo_image.zip` (one image) or `Test_files/Test.zip` (10 images).

To use the app with your own images, put your JPEG or PNG files in a `.zip` archive. Upload by dragging the archive onto the drop zone or <i>Browse local files</i>. Results appear when the whole processing is done.

Review predictions:

- see the crop and click it to zoom in
- choose another species among the top 5 suggested identifications
- type your own label
- delete a false positive

> Edits live in your browser tab only. Refreshing the page or uploading a new zip discards them, so download your results before you leave.

## Credits and citation

D.U.D.E. is built on the work of others. If you use it in research, please cite the underlying projects:

- **Flat-Bug**: <https://github.com/darsa-group/flat-bug>
- **BioCLIP 2** and the TreeOfLife-200M dataset: <https://github.com/Imageomics/bioclip-2>
- **pybioclip**: <https://github.com/Imageomics/pybioclip>

See each project's repository for the recommended citation and for the license terms of the model weights and data, which are separate from this repository's license.
