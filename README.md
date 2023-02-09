<img src="./figurl.png" width="200px" />

# figurl

Figurl is a framework for creating browser-based, shareable, interactive views of scientific datasets in the cloud. It is designed to be used in collaborative environments, such as scientific research teams, and is built on top of [Kachery cloud](https://github.com/flatironinstitute/kachery-cloud).

[Introduction to Figurl](./doc/intro.md)

[Gallery of examples](https://magland.github.io/figurl-gallery-viewer/)

> This package is intended for collaborative sharing of data for scientific research. It should not be used for other purposes. At this point, uploaded files are not guaranteed to be available for ever. Contact us if you are interested storing files using your own cloud resources.

## Installation and setup

> Note: most of the time, you will be using a different Python package that includes figurl as a dependency. But you can also install figurl directly and use the basic static functionality (Altair charts, markdown documents, reports).

It is recommended that you use a conda environment with Python >= 3.8 and numpy.

```bash
pip install --upgrade figurl
```

Configure your [kachery-cloud](https://github.com/flatironinstitute/kachery-cloud) client

```bash
kachery-cloud-init
# follow the instructions to associate your client with your GitHub user name on kachery-cloud
```

## Static examples

To test the system, try running the scripts in the [examples/](./examples/) folder. Here are the example (static) figures:

* [Altair chart](https://figurl.org/f?v=gs://figurl/vegalite-2&d=sha1://0369af9f1a54a5a410f99e63cb08b6b899d1c92f&label=stocks%20chart)
* [Markdown document](https://figurl.org/f?v=gs://figurl/markdown-1&d=sha1://9fe1d643f883e1676f70082b679c8a825b879041&label=Example%20markdown)
* [Report](https://figurl.org/f?v=gs://figurl/figurl-report&d=sha1://e0f267258f432adcb89c5379c4136c3f00fbce78&label=Example%20report)

Each of these links pair a visualization plugin (`v` query parameter) with a piece of data (`d` query parameter). For example, the Altair chart figURL:

https://figurl.org/f?v=gs://figurl/vegalite-2&d=sha1://0369af9f1a54a5a410f99e63cb08b6b899d1c92f&label=stocks%20chart

## Interactive examples

For examples of interactive figures, see [intro to Figurl](./doc/intro.md).

## How it works

![image](https://user-images.githubusercontent.com/3679296/201342587-b1af33bd-ac2b-4f9f-9cfa-3a0c0ce6d23b.png)

* Python script assembles the data and figure specifications.
* Data are uploaded to a content-addressable storage database in the cloud ([Kachery](https://github.com/flatironinstitute/kachery-cloud)).
* Python script generates a URL that pairs a visualization plugin (hosted in a cloud storage bucket) and the uploaded data.
* The shareable URL takes the user to figurl.org where the data is downloaded and sent to the visualization plugin for display.

## Cloud storage

By default, your data files will be stored using our cloud resources, and they are not guaranteed to be available forever. You can also configure figurl to use your own resources by [creating a Kachery zone](https://github.com/flatironinstitute/kachery-cloud/blob/main/doc/create_kachery_zone.md).

## Contributing

* Star us on GitHub
* Provide feedback
* Contact us if you would like to help develop and maintain this open source project

## For developers

[Embedded figure protocol](./doc/embedded_figure_protocol.md)

## Authors

Jeremy Magland and Jeff Soules, [Center for Computational Mathematics, Flatiron Institute](https://www.simonsfoundation.org/flatiron/center-for-computational-mathematics)

## License

Apache 2.0
