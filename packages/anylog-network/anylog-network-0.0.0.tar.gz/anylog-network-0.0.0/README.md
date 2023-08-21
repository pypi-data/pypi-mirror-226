# AnyLog Network

<div align="center">
    <img src="https://github.com/AnyLog-co/documentation/blob/master/imgs/anylog_logo.png" />
</div>

AnyLog provides Real-Time Visibility and Management of Distributed Edge Data, Applications and Infrastructure. AnyLog 
transforms the edge to a scalable data tier that is optimized for IoT data, enabling organizations to extract real-time 
insight for any use case in any industries spanning Manufacturing, Utilities, Oil & Gas, Retail, Robotics, Smart Cities, 
Automotive, and more.

With AnyLog deployed on edge nodes, the nodes become members of a peer-to-peer (P2P) network that provides access to 
distributed IoT data from a single point, as if the data is organized and unified on a single machine. This approach 
creates two tiers: a physical tier that automates data management on the edge nodes, and a virtualized tier that 
provides access to the distributed data from a single point. This approach provides a cloud-like setup for the 
distributed edge making IoT data available in real time anywhere, anytime and for any use case, without the need to move 
the data and without locking customers into specific clouds, applications or hardware.

To receive additional info, email to: [info@anylog.co](mailto:info@anylog.co)

## Deployment
**Note Types**:
* Master – A node that manages the shared metadata (if a blockchain platform is used, this node is redundant).
* Operator – A node that hosts the data. For this deployment we will have 2 Operator nodes.
* Query – A node that coordinates the query process. 
* Publisher - A node that supports distribution of data from device(s) to operator nodes. This node is not part of the
deployment diagram. However, is often used in large scale projects. 

**Deployment Diagram**:

![deployment diagram](https://github.com/AnyLog-co/documentation/blob/master/imgs/deployment_diagram.png)

## AnyLog Versions
AnyLog has 3 major versions, each version is built on both _Ubuntu:20.04_ with _python:3.9-alpine_. 
* develop - is a stable release that's been used as part of our Test Network for a number of weeks, and gets updated every 4-6 weeks.
* predevelop - is our beta release, which is being used by our Test Network for testing purposes.
* testing - Any time there's a change in the code we deploy a "testing" image to be used for (internal) testing purposes.
* Usually the image will be Ubuntu based, unless stated otherwise.


| Build             | Base Image          | CPU Architecture | Pull Command                                            | Compressed Size | 
|-------------------|---------------------|---|---------------------------------------------------------|-----------------|
| develop           | Ubuntu:20.04        | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:develop`           | ~320MB                | 
| develop-alpine    | python:3.9-alpine   | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:develop-alpine`    | ~170MB                |
| develop-rhl       | redhat/ubi8:latest  | amd64,arm64 | `docker pull anylogco/anylog-network:develop-rhl`       |  ~215MB               |
| predevelop        | Ubuntu:20.04        | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:predevelop`        | ~320MB          | 
| predevelop-alpine | python:3.9-alpine   | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:predevelop-alpine` | ~170MB          |
| predevelop-rhl    | redhat/ubi8:latest   | amd64,arm64 | `docker pull anylogco/anylog-network:predevelop-rhl`    | ~215MB          |
| testing           | Ubuntu:20.04        | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:testing`           |

*Compressed Size - size calculated by summing the image's layers, which are compressed


By default, the AnyLog image is configured to run as a _REST_ node, which means that the TCP and REST options 
are running, but no other process is enabled. This allows for users to play with the system with no other services 
running in the background, but already having the default network configurations.  A basic deployment of an AnyLog REST 
instance can be  executed using the following line:

**Docker Deployment**
```shell
docker run --network host -it --detach-keys="ctrl-d" --name anylog-node --rm anylogco/anylog-network:develop
```

**Kubernetes Deployment**
```shell
git clone https://github.com/AnyLog-co/deployments 
helm install $HOME/helm/packages/anylog-node-volume-1.22.3.tgz --name-template anylog-node-volume 
helm install    $HOME/helm/packages/anylog-node-1.22.3.tgz --name-template anylog-node
```



