<p align="center">
  <img src="./cover.jpg" alt="Car recommending products"/>
</p>
<h1 align="center">
  A simple Gen AI Product Recommendation System that is designed for rapid proof-of-concept (POC) development.
  <br>
</h1>

<h4 align="center">Let's build a simple Gen AI Product Recommendation System that can be used for a proof-of-concepts (POC) to recommend products to your customers </h4>

<h4 align="center">This is the companion repo for this blog article . Please refer to it if you would like more information about this process.</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#license">License</a> •
  <a href="#contact">Contact</a>
</p>

## Key Features

- Only uses Python and now other languages or frameworks
- Uses a CSV file as the data source
    - More on the CSV file in the next section
- The only pre-req is an Azure subscription with Azure Open AI

## Pre-req Azure components

This repo has the code to run this process, but there are some pre-req components that need to be created in Azure before you can run it.

- An Azure subscription :)
- An Azure Open AI resource
    - I use the text-embedding-ada-002 model to vectorise the CSV file and creat text embeddings
    - I use the GPT-4o model to recommend the next best product

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com) installed on your computer.

```bash
# 1. Clone this repository
$ git clone https://github.com/fredderf204/poc-recsys

# 2. Go into the repository
$ cd poc-recsys

# 3. Run the code
$ python3 -m venv .venv
$ pip install -r requirements.txt
click on function_app.py
click on the debug icon.
```

## License

MIT License

Copyright (c) [2023] [Michael Friedrich]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Contact

> LinkedIn [Michael Friedrich](https://www.linkedin.com/in/1michaelfriedrich/) &nbsp;&middot;&nbsp;
> GitHub [fredderf204](https://github.com/fredderf204) &nbsp;&middot;&nbsp;
> Twitter [@fredderf204](https://twitter.com/fredderf204)