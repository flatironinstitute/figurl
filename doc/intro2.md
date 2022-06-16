# Introduction to Figurl

Figurl offers **browser-based**, **shareable**, **interactive** views of scientific
datasets in the cloud.

## Concept

> Generate a figURL (permalink) to an interactive visualization from any Python script
* Generate from anywhere: workstation, notebook, continuous integration, etc.
* Minimal configuration

> Data needed for the visualization is stored in the cloud
* See [kachery-cloud](https://github.com/scratchrealm/kachery-cloud)
* Content-addressable storage
* Configurable backend storage: Google, AWS, Wasabi, Filebase

> Visualization plugin stored in cloud
* Versioned HTML bundle
* ReactJS / typescript - highly recommended but not strictly required

> The URL points to the data and the visualization plugin
* Data is referenced via content-hash URI
* Visualization plugin is a static, versioned HTML bundle and is referenced by URI to a cloud bucket

> The figurl web app (figurl.org) pairs the data with the visualization and presents the interactive view to the user
* Manages loading of data objects from the cloud
* Renders the visualization plugin in an embedded iframe
* Handles advanced capabilities of the figure
  - User login (e.g., for curation)
  - Lazy loading of additional data objects
  - Live feeds (for real-time updates or curation)
  - Task backends (for on-demand computation)