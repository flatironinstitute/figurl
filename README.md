<img src="./figurl.png" width="200px" />

# figurl

> :warning: This project is in BETA.

> **IMPORTANT**: This package is intended for collaborative sharing of data for scientific research. It should not be used for other purposes.

Browser-based, shareable, interactive views of scientific
datasets in the cloud.

[Introduction and overview (including examples)](./doc/intro.md)

See also [kachery-cloud](https://github.com/flatironinstitute/kachery-cloud)

## Installation and setup

> Note: most of the time, you will be using a different Python package that includes figurl as a dependency. But you can also install figurl directly and use the basic functionality (Altair charts, reports, log tables, etc).

It is recommended that you use a conda environment with Python >= 3.8 and numpy.

```bash
pip install --upgrade figurl
```

Configure your [kachery-cloud](https://github.com/flatironinstitute/kachery-cloud) client

```bash
kachery-cloud-init
# follow the instructions to associate your client with your Google user name on kachery-cloud
```

To test the system, try running the scripts in the [examples/](./examples/) folder.

## Cloud storage

By default, your data will be stored in our inexpensive cloud buckets, and it is not guaranteed to be available forever. You can also configure figurl to use your own storage buckets. For more information, see [kachery-cloud](https://github.com/flatironinstitute/kachery-cloud).

## Information for developers

See [figurl2-gui](https://github.com/scratchrealm/figurl2-gui)

## Authors

Jeremy Magland and Jeff Soules, [Center for Computational Mathematics, Flatiron Institute](https://www.simonsfoundation.org/flatiron/center-for-computational-mathematics)

## License

Apache 2.0
